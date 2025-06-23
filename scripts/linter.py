import re

# Constants
SEVERITY_HEADERS = ["## High", "## Medium", "## Low", "## Informational", "## Gas Optimization"]
SUBSECTION_HEADERS = {
    "## Summary": "**Summary:**",
    "## Description": "**Description:**", 
    "## Impact Explanation": "**Impact Explanation:**",
    "## Likelihood Explanation": "**Likelihood Explanation:**", 
    "## Recommendation": "**Recommendation:**",
    "## Proof of Concept": "**Proof of Concept:**"
}
HEADERS_NEEDING_NEWLINE = ["## Description", "## Recommendation"]


def replace_org_in_link(line, internal_org, internal_repo_name, source_org, source_repo_name):
    """Replace internal organization links with source organization links."""
    links = re.findall(r'https?://[^\s<>"]+|[^\s<>"]+\.[^\s<>"]+', line)

    for link in links:
        if re.search(internal_org, link, re.IGNORECASE):
            new_link = re.sub(internal_org, source_org, link, flags=re.IGNORECASE)
            if source_repo_name != internal_repo_name:
                new_link = re.sub(internal_repo_name, source_repo_name, new_link, flags=re.IGNORECASE)
            line = line.replace(link, new_link)

    return line


def replace_ampersand_in_findings_headings(line):
    """Replace '&' with 'and' in finding headings."""
    if line.strip().startswith('###') and '&' in line:
        return line.replace('&', 'and')
    return line


def find_severity_sections(report):
    """Find all severity section line indices."""
    severity_sections = []
    
    # Find bare ## markers followed by findings
    for i, line in enumerate(report):
        if line.strip() == "##":
            # Look ahead for finding headings (###)
            for j in range(i + 1, min(i + 5, len(report))):
                if report[j].strip().startswith("###"):
                    severity_sections.append(i)
                    break
    
    # Find existing proper severity headers
    for i, line in enumerate(report):
        if line.strip() in SEVERITY_HEADERS and i not in severity_sections:
            severity_sections.append(i)
    
    return sorted(severity_sections)


def assign_severity_labels(report, severity_sections):
    """Assign appropriate severity labels to sections."""
    severity_labels = []
    
    for idx, section_line in enumerate(severity_sections):
        current_line = report[section_line].strip()
        
        if current_line in SEVERITY_HEADERS:
            severity_labels.append((section_line, current_line))
        else:
            # Assign based on position, with fallback to Low
            if idx < len(SEVERITY_HEADERS):
                severity_labels.append((section_line, SEVERITY_HEADERS[idx]))
            else:
                severity_labels.append((section_line, "## Low"))
    
    return severity_labels


def fix_basic_formatting(report, internal_org, internal_repo_name, source_org, source_repo_name):
    """Apply basic line-by-line formatting fixes."""
    for i, line in enumerate(report):
        # Apply all basic transformations
        line = replace_org_in_link(line, internal_org, internal_repo_name, source_org, source_repo_name)
        line = replace_ampersand_in_findings_headings(line)
        line = line.replace('\\\\', '\\')  # GitHub MathJax to LaTeX
        report[i] = line


def fix_severity_headers(report):
    """Fix severity section headers."""
    severity_sections = find_severity_sections(report)
    severity_labels = assign_severity_labels(report, severity_sections)
    
    for line_index, severity_label in severity_labels:
        current_line = report[line_index].strip()
        if current_line == "##" or current_line in ["## nal", "## zation"]:
            report[line_index] = severity_label
    
    # Fix any remaining truncated headers
    for i, line in enumerate(report):
        stripped_line = line.strip()
        if stripped_line == "## nal":
            report[i] = "## Informational"
        elif stripped_line == "## zation":
            report[i] = "## Gas Optimization"


def split_headers_with_content(report):
    """Split headers that have content on the same line."""
    i = 0
    while i < len(report):
        line = report[i].strip()
        
        for pattern in SUBSECTION_HEADERS.keys():
            if line.startswith(pattern) and len(line) > len(pattern) + 1:
                content = line[len(pattern):].strip()
                report[i] = pattern
                
                if content:
                    report.insert(i + 1, "")
                    report.insert(i + 2, content)
                break
        
        i += 1


def convert_subsection_headers(report):
    """Convert sub-section headers to inline bold format."""
    i = 0
    while i < len(report):
        line = report[i].strip()
        
        if line in SUBSECTION_HEADERS:
            bold_header = SUBSECTION_HEADERS[line]
            content_lines = collect_content_lines(report, i + 1)
            
            if content_lines:
                process_content_lines(report, i, line, bold_header, content_lines)
            else:
                # No content found, just replace with bold header
                report[i] = bold_header
                if line in HEADERS_NEEDING_NEWLINE:
                    report.insert(i + 1, "")
        
        i += 1


def collect_content_lines(report, start_index):
    """Collect content lines following a header until next header or clearpage."""
    content_lines = []
    j = start_index
    
    # Skip blank lines after header
    while j < len(report) and report[j].strip() == "":
        j += 1
    
    # Collect content until next header or clearpage
    while j < len(report):
        next_line = report[j].strip()
        if next_line.startswith("##") or next_line.startswith("###") or "\\clearpage" in next_line:
            break
        content_lines.append(report[j])
        j += 1
    
    # Remove trailing empty lines
    while content_lines and content_lines[-1].strip() == "":
        content_lines.pop()
    
    return content_lines


def process_content_lines(report, header_index, original_header, bold_header, content_lines):
    """Process and replace content lines with inline format."""
    if not content_lines:
        return
    
    first_content_line = content_lines[0].strip()
    
    # Calculate how many lines to remove (header + collected content)
    lines_to_remove = len(content_lines)
    
    # Find the actual end of content in the report by counting non-empty lines
    content_start = header_index + 1
    while content_start < len(report) and report[content_start].strip() == "":
        content_start += 1
    
    # Remove original content lines (but keep the header line for replacement)
    for _ in range(lines_to_remove):
        if content_start < len(report):
            del report[content_start]
    
    if first_content_line:
        # Join first content line with bold header
        report[header_index] = f"{bold_header} {first_content_line}"
        
        # Add remaining content lines
        for k, content_line in enumerate(content_lines[1:], 1):
            report.insert(header_index + k, content_line)
        
        # Add newline after Description/Recommendation
        if original_header in HEADERS_NEEDING_NEWLINE:
            content_end_index = header_index + len(content_lines)
            report.insert(content_end_index, "")
    else:
        # First line is empty, use bold header alone
        report[header_index] = bold_header
        for k, content_line in enumerate(content_lines, 1):
            report.insert(header_index + k, content_line)
        
        if original_header in HEADERS_NEEDING_NEWLINE:
            content_end_index = header_index + len(content_lines) + 1
            report.insert(content_end_index, "")


def check_link_issues(report):
    """Check for potential link issues and report them."""
    for i, line in enumerate(report):
        # Check for broken link structures
        pos = line.find("](")
        while pos != -1:
            if line[pos+2:pos+6] != "http" and line[pos+2] != "#":
                print(f"Possible broken link at report.md line {i+1}: ")
                print(f"\t{line.strip()}")
            pos = line.find("](", pos+1)

        # Check for raw links
        pos = line.find("http")
        while pos != -1:
            if pos >= 2 and line[pos-2:pos] != "](":
                print(f"Possible raw link at report.md line {i+1}: ")
                print(f"\t{line.strip()}")
            pos = line.find("http", pos+1)


def clean_excessive_blank_lines(report):
    """Remove excessive consecutive blank lines (more than 2)."""
    i = 0
    while i < len(report) - 2:
        if (report[i].strip() == "" and 
            report[i + 1].strip() == "" and 
            report[i + 2].strip() == ""):
            del report[i + 1]
        else:
            i += 1


def lint(report, team_name, source_org, source_repo_name, internal_org, internal_repo_name):
    """Main linting function that applies all formatting fixes."""
    # Apply all linting passes
    fix_basic_formatting(report, internal_org, internal_repo_name, source_org, source_repo_name)
    fix_severity_headers(report)
    split_headers_with_content(report)
    convert_subsection_headers(report)
    check_link_issues(report)
    clean_excessive_blank_lines(report)

    return report