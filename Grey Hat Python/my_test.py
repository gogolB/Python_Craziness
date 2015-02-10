import my_debugger

debugger = my_debugger.debugger()

pid = input("Enter PID of process to attach to: ")

debugger.attach(int(pid))

printf_address = debugger.func_resolve("msvcrt.dll".encode("ASCII"), "printf".encode("ASCII"))

print("[*] Address of printf: 0x%08x" % printf_address)

debugger.bp_set(printf_address)

debugger.run()

debugger.detach()
