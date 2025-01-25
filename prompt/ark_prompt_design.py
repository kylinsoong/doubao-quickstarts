import os

python_files = [
  "ark_prompt_design_focus_1.py",
  "ark_prompt_design_focus_2.py",
  "ark_prompt_design_separator.py",
  "ark_prompt_design_structure.py",
  "ark_prompt_design_format.py",
]

for file in python_files:
    try:
        os.system(f"python3 {file}")
        print()
    except Exception as e:
        print(f"Error running {file}: {e}")
