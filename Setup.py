import cx_Freeze

executables = [cx_Freeze.Executable("Main.py")]

cx_Freeze.setup(
    name="Bizarre Car",
    options={
        "build_exe":
            {"packages": ["pygame"],
             "include_files": ["Car.png","speed.png", "Retrow Mentho.ttf", "reggae.wav", "Crash.wav"]}},
    executables=executables
)
