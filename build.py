import os
import subprocess
import shutil
import sys
from pathlib import Path
import time
import pkg_resources

VERSION = "1.0.0"
APP_NAME = "Silent Bloom"

def print_step(step, message):
    """Print a formatted step message"""
    print(f"\n[{step}] {message}")
    sys.stdout.flush()

def check_dependencies():
    """Check if all required dependencies are installed"""
    print_step("CHECK", "Verifying dependencies...")
    
    required_packages = {
        "Pillow": "pillow",
        "PyInstaller": "pyinstaller"
    }
    
    missing_packages = []
    
    for display_name, pkg_name in required_packages.items():
        try:
            pkg_resources.get_distribution(pkg_name)
            print(f"✓ {display_name} is installed")
        except pkg_resources.DistributionNotFound:
            missing_packages.append(pkg_name)
            print(f"✗ {display_name} is missing")
    
    if missing_packages:
        print("\nPlease install missing dependencies:")
        print("pip install " + " ".join(missing_packages))
        return False
    
    return True

def generate_icon():
    """Generate the application icon"""
    print_step("ICON", "Generating application icon...")
    
    try:
        subprocess.run([sys.executable, "icon.py"], check=True)
        if not os.path.exists("icon.ico"):
            raise Exception("Icon file was not generated")
        print("✓ Icon generated successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to generate icon: {e}")
        return False

def check_nircmd():
    """Check if nircmd.exe exists"""
    print_step("CHECK", "Verifying NirCmd...")
    
    if not os.path.exists("nircmd.exe"):
        print("✗ nircmd.exe not found in the current directory")
        return False
    
    print("✓ nircmd.exe found")
    return True

def clean_build_files():
    """Clean up build artifacts"""
    print_step("CLEAN", "Cleaning up build artifacts...")
    
    paths_to_remove = [
        "build",
        "dist",
        "silent_bloom.spec",
        "__pycache__"
    ]
    
    for path in paths_to_remove:
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"✓ Removed file: {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"✓ Removed directory: {path}")
        except Exception as e:
            print(f"✗ Failed to remove {path}: {e}")
            # Don't return False here, continue with other files
    
    return True  # Return True even if some files couldn't be removed

def build_executable():
    """Build the executable using PyInstaller"""
    print_step("BUILD", f"Building {APP_NAME} v{VERSION}...")
    
    try:
        # Create version info file
        version_info = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({','.join(VERSION.split('.'))},0),
    prodvers=({','.join(VERSION.split('.'))},0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u''),
         StringStruct(u'FileDescription', u'{APP_NAME}'),
         StringStruct(u'FileVersion', u'{VERSION}'),
         StringStruct(u'InternalName', u'silent_bloom'),
         StringStruct(u'LegalCopyright', u''),
         StringStruct(u'OriginalFilename', u'silent_bloom.exe'),
         StringStruct(u'ProductName', u'{APP_NAME}'),
         StringStruct(u'ProductVersion', u'{VERSION}')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        with open("version_info.txt", "w") as f:
            f.write(version_info)

        # Build command
        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            f"--version-file=version_info.txt",
            "--icon=icon.ico",
            "--add-binary=nircmd.exe;.",
            "--name=silent_bloom",
            "silent_bloom.py"
        ]
        
        subprocess.run(cmd, check=True)
        print("✓ Build completed successfully")
        
        # Verify the executable was created
        exe_path = os.path.join("dist", "silent_bloom.exe")
        if not os.path.exists(exe_path):
            raise Exception("Executable was not created")
        
        print(f"\n✓ Executable created: {exe_path}")
        print(f"✓ Size: {os.path.getsize(exe_path) / 1024 / 1024:.1f} MB")
        return True
        
    except Exception as e:
        print(f"✗ Build failed: {e}")
        return False
    finally:
        # Clean up version info file
        if os.path.exists("version_info.txt"):
            os.remove("version_info.txt")

def main():
    """Main build process"""
    start_time = time.time()
    
    print(f"\n=== Building {APP_NAME} v{VERSION} ===\n")
    
    # Create dist directory if it doesn't exist
    os.makedirs("dist", exist_ok=True)
    
    # Run build steps
    steps = [
        ("Dependencies", check_dependencies),
        ("NirCmd", check_nircmd),
        ("Cleanup", clean_build_files),
        ("Icon", generate_icon),
        ("Build", build_executable)
    ]
    
    success = True
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n✗ Build failed at {step_name} step")
            success = False
            break
    
    # Final cleanup
    if os.path.exists("version_info.txt"):
        os.remove("version_info.txt")
    
    # Print build summary
    duration = time.time() - start_time
    print(f"\n=== Build Summary ===")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Status: {'Success' if success else 'Failed'}")
    
    if success:
        print(f"\nExecutable is ready: dist/silent_bloom.exe")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 