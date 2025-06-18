import re


def replace_org_in_link(line, internal_org, internal_repo_name, source_org, source_repo_name):
    # Identify all links
    links = re.findall('https?://[^\s<>"]+|[^\s<>"]+\.[^\s<>"]+', line)

    for link in links:
        if re.search(internal_org, link, re.IGNORECASE):
            # Replace internal organization with source organization
            new_link = re.sub(internal_org, source_org, link, flags=re.IGNORECASE)

            # Replace internal repository name with source repository name, if different
            if source_repo_name != internal_repo_name:
                new_link = re.sub(internal_repo_name, source_repo_name, new_link, flags=re.IGNORECASE)
            
            line = line.replace(link, new_link)

    return line


def replace_ampersand_in_findings_headings(line):
    # If the line is a finding markdown heading and contains '&', replace '&' with 'and'
    if line.strip().startswith('###') and '&' in line:
        line = line.replace('&', 'and')

    return line


def lint(report, team_name, source_org, source_repo_name, internal_org, internal_repo_name):
    for i, line in enumerate(report):
        new_line = line
        
        # Replace any internal organization repo links
        new_line = replace_org_in_link(new_line, internal_org, internal_repo_name, source_org, source_repo_name)
        
        # Replace any '&' in finding headings with 'and'
        new_line = replace_ampersand_in_findings_headings(new_line)

        # Replace any double backslashes with single backslashes (GitHub MathJax to LaTeX)
        new_line = new_line.replace('\\\\', '\\')

        report[i] = new_line

    # Check for link structures ( format [something](url) ) that don't start with http
    for i, line in enumerate(report):
        pos = line.find("](")
        while pos != -1:
            # Check if the first 4 characters after the open-paren are "http"
            if pos + 6 < len(line) and line[pos+2:pos+6] != "http" and line[pos+2] != "#":
                print(f"Possible broken link at report.md line {i+1}: ")
                print(f"\t{line.strip()}")
            pos = line.find("](", pos+1)

    # Check for raw links ("http" string not immediately preceded by a link structure)
    for i, line in enumerate(report):
        pos = line.find("http")
        while pos != -1:
            # Check if the character to the left of "http" is an open-paren preceded by a close-bracket
            if pos >= 2 and line[pos-2:pos] != "](":
                print(f"Possible raw link at report.md line {i+1}: ")
                print(f"\t{line.strip()}")
            pos = line.find("http", pos+1)

    # Check for descriptions not starting in the same line as the headers
    lineNumber = 0
    while lineNumber < len(report):
        line = report[lineNumber]
        
        # Check for headers that should have content on the same line
        should_merge = False
        header_patterns = [
            "## Summary",
            "## Description", 
            "## Impact Explanation",
            "## Likelihood Explanation", 
            "## Recommendation",
            "## Proof of Concept",
            f"**{internal_org}:**",
            f"**{team_name}:**"
        ]
        
        for pattern in header_patterns:
            if line.startswith(pattern) and len(line.strip()) <= len(pattern) + 3:
                should_merge = True
                break
        
        if should_merge:
            # There might be more than one empty lines following the header, remove them
            while lineNumber + 1 < len(report) and report[lineNumber + 1].strip() == "":
                del report[lineNumber + 1]

            if lineNumber + 1 < len(report):
                nextLine = report[lineNumber + 1]
                # If it's a list, code block, quote, or another header, don't merge
                if (not nextLine.lstrip().startswith("-") and
                    not nextLine.lstrip().startswith("1.") and
                    not nextLine.lstrip().startswith("```") and
                    not nextLine.lstrip().startswith("#") and
                    not nextLine.lstrip().startswith(">") and
                    not nextLine.lstrip().startswith("*")):

                    report[lineNumber] = line + " " + nextLine.lstrip()
                    del report[lineNumber + 1]
                    continue  # Don't increment lineNumber since we deleted a line

        lineNumber += 1

    # Clean up excessive blank lines (more than 2 consecutive)
    i = 0
    while i < len(report) - 2:
        if (report[i].strip() == "" and 
            report[i + 1].strip() == "" and 
            report[i + 2].strip() == ""):
            # Found 3+ consecutive blank lines, remove one
            del report[i + 1]
        else:
            i += 1

    # Ensure severity section headers are properly formatted
    for i, line in enumerate(report):
        # Fix severity headers that are just "##" or have partial text
        if line.strip() == "##":
            # Look ahead to see if this is followed by finding titles
            if i + 1 < len(report) and report[i + 1].strip().startswith("###"):
                # This appears to be a severity section marker, keep as is
                continue
        elif line.strip() in ["## nal", "## zation"]:
            # These appear to be truncated severity markers, expand them
            if "nal" in line:
                report[i] = "## Informational"
            elif "zation" in line:
                report[i] = "## Gas Optimization"

    return report