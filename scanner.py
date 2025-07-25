import socket
from colorama import init, Fore, Style
import threading # Boost the spped when tasks are independent
import datetime
import sqlite3


init()
DB_FILE = 'scanner.db'
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                port INTEGER,
                status TEXT,
                banner TEXT,
                timestamp TEXT
              )
              ''')
    conn.commit()
    conn.close()
    

def grab_banner(sock):
    try:
        banner = sock.recv(1024)
        return banner.decode().strip()
    
    except:
        return None

def scan_port(ip, port, output_file, file_lock, db_conn, db_lock):
        # AF_INET: tells Python using IPv4
        # SOCK_STREAM: using TCP protocol (reliable, connection-based)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # if the connection takes longer than 0.5s -> give up and move on
        result = sock.connect_ex((ip, port))
        
        banner = None
        status = "open" if result == 0 else "closed"

        if status == 'open':
            print(f"{Fore.GREEN}[+] Port {port} is open {Style.RESET_ALL}")
            banner = grab_banner(sock)

            with file_lock:
                output_file.write(f"[+] Port {port} is open\n")
                if banner:
                    print(f"{Fore.CYAN}    [Banner] {banner}{Style.RESET_ALL}")
                    output_file.write(f"    [Banner] {banner}\n")
                else:
                    print(f"{Fore.YELLOW}[No banner received] {Style.RESET_ALL}")
                    output_file.write(f"[No banner received] \n")

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with db_lock:
                c = db_conn.cursor()
                c.execute('INSERT INTO scans (ip, port, status, banner, timestamp) VALUES(?, ?, ?, ?, ?)',
                            (ip, port, status, banner, timestamp))
                db_conn.commit()

        except Exception as e:
            print(f'[!] Database insert error: {e}')

        sock.close()

def scanner():
    init_db()
    with open("targets.txt", "r") as ip_file:
        targets = [line.strip() for line in ip_file if line.strip()]

    port_range = input("Enter port range (e.g., 20-80): ")
    start_port, end_port = map(int, port_range.split('-'))

    file_lock = threading.Lock()
    db_lock = threading.Lock()


    db_conn = sqlite3.connect(DB_FILE, check_same_thread=False) # Allows connection sharing between threads
    
    try:
        with open("scan_results.txt", "w") as output_file:
            for ip in targets:
                print(f"{Fore.RED}=== Scanning {ip} === {Style.RESET_ALL}")
                output_file.write(f"=== Results for {ip} === \n")

                threads = []
                for port in range(start_port, end_port + 1):
                    t = threading.Thread(target=scan_port, args=(ip, port, output_file, file_lock, db_conn, db_lock))
                    t.start()
                    threads.append(t)

                # Waiting for all threads to finish before exiting
                for t in threads:
                    t.join()
    except IOError as e:
        print(f"[!] Failed to write results: {e}")
    finally:
        db_conn.close()

    print('Results saved in scan_results.txt and in scanner.db')
scanner()
