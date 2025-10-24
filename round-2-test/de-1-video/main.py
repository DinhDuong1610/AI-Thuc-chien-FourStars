# main.py
from tasks.generate_outline import generate_outline
from tasks.generate_script_mc import generate_script_mc
from tasks.generate_images import generate_images
from tasks.generate_tts import generate_tts

def main():
    print("🎬 STARTING AI THỰC CHIẾN - ĐỀ 1 PIPELINE\n")
    generate_outline()
    generate_script_mc()
    generate_images()
    generate_tts()
    print("\n🏁 DONE! Check folder outputs/ for all files.")

if __name__ == "__main__":
    main()
