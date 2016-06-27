def ask_quit(prompt, retries=4, complaint='Yes or no, please!'):
    while True:
        ok = raw_input(prompt)
        if ok in ('y', 'ye', 'yes','Y'):
            return True
        if ok in ('n', 'no', 'nop', 'nope','N'):
            return False
        retries -= 1
        if retries < 0:
            raise IOError('refusenik user')
        print complaint


#se usa llamando a ask_quit('Lo que quieras que diga')
