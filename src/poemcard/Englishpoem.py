import argparse
import sys
from generator import generate_poem
from validation import validate_poem  
from visualizer import render_card   


def main():
  parser = argparse.ArgumentParser(description="Acrostic Poem System - All-in-One English Acrostic CLI"  )
  parser.add_argument("word", type=str, help="Acrostic word (3–8 English letters, e.g., CODE)" )
  parser.add_argument("--theme", type=str, required=True, help="Poem theme (e.g., Python debugging)")
  parser.add_argument("--output",type=str,default="poem.png",help="Output path for the exported poem card PNG (default: poem.png)",)
  args = parser.parse_args()

  print(f"\n [Pipeline] Command received -> Acrostic word: {args.word} | Theme: {args.theme}")
  # Step 1: Calling generation module
  
  print("Step 1: Calling generation module...")
  try:
    poem_lines = generate_poem(args.word, args.theme)
  except Exception as e:
    print(f" Generation module error: {e}")
    sys.exit(1)
  # Step 2: Calling validation module
  print("Step 2: Calling validation module...")
  errors = validate_poem(args.word, poem_lines)
  if errors:      
    print(" Validation check failed:")
    for err in errors:
        print(f" -{err}")
    sys.exit(1)
  print(" Validation passed!")
#正式版可删
  # 3. Used for previewing in the terminal
  print("\n" + "=" * 40)
  for line in poem_lines:
    print("  ", line)
  print("=" * 40 + "\n")

  # Step 3: Invoking real visual rendering and export module
  print(f"Step 3: Invoking layout & rendering module, exporting to {args.output}...")
  try:
    # Generating PNG
    render_card(poem_lines, args.output)
    print(f" Success! Poem card rendered and saved to local file:  {args.output}")
  except Exception as e:
    print(f" Failed to render or export image: {e}")
    sys.exit(1)
#正式版可删
  print("\n Clear！\n")


if __name__ == "__main__":
  main()





