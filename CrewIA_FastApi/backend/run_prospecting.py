import subprocess
import time
from datetime import datetime
import re

def run_crew():
    """Runs the crewai crew."""
    try:
        # We use shell=True to be able to use the `crewai` command directly
        # as if we were in a shell.
        subprocess.run("crewai run", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the crew: {e}")

def extract_prospect_info(report_content):
    """Extracts prospect information from the report."""
    # This regex is designed to capture the prospect information block
    # It looks for a markdown block starting with the prospect list
    # and captures everything until the next section.
    match = re.search(r"## 2. Liste (?:Complète des )?Prospects Identifiés\s*\n(.*?)\n## 3.", report_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def main():
    """Main function to run the prospecting loop."""
    prospects_list_file = "prospects_list.md"
    target_prospects = 50

    # Initialize the prospects list file
    with open(prospects_list_file, "w") as f:
        f.write("# Liste des Prospects\n\n")

    for i in range(target_prospects):
        print(f"--- Running iteration {i+1}/{target_prospects} ---")
        
        run_crew()
        
        try:
            with open("report.md", "r") as f:
                report_content = f.read()
            
            print("--- Content of report.md ---")
            print(report_content)
            print("--------------------------")
            
            prospect_info = extract_prospect_info(report_content)
            
            if prospect_info:
                with open(prospects_list_file, "a") as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"## Prospect {i+1} - Ajouté le {timestamp}\n\n")
                    f.write(prospect_info)
                    f.write("\n\n---\n\n")
                print(f"Prospect {i+1} added to {prospects_list_file}")
            else:
                print("Could not extract prospect information from report.md")

        except FileNotFoundError:
            print("report.md not found. Skipping this iteration.")
            
        print("Waiting for 1 minute before the next run...")
        time.sleep(60)

    print(f"--- Prospecting complete. {target_prospects} prospects generated. ---")

if __name__ == "__main__":
    main()
