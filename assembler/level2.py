#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) < 2:
    print 'Usage: python %s <inputfile>' % sys.argv[0]
    exit(1)

inputfile = open(sys.argv[1]).read()

alu = ['add', 'mul', 'div', 'mod', 'or']

for line in inputfile.split('\n')[:-1]:
    try:
        if not line.split('//')[0].split():
            print line
            continue
        if '//' in line:
            line = line[:line.find('//')]
        command = line.split()[0]
        args = line.split()[1:]

        # in-line assembler
        if command in ['st', 'rd', 'wr', 'al', 'cp', 'jz']:
            print line
        
        elif command == 'set':
            value = args[-1]
            if value.startswith('0x'):
                value = int(value, 16)
            elif value.startswith('0b'):
                value = int(value, 2)
            else:
                value = int(value)
            value = (value % 256 + 256) % 256
            if len(args) > 1:
                print 'st %s %i' % (args[0], value)
            else:
                print 'st %i' % value

        elif command == 'read' or command == 'write':
            variable = args[-1]
            if '[' in variable:
                variable, i = variable.split('[')
                i = i.split(']')[0]
                if i.isdigit():
                    print 'st l %s' % i
                else:
                    print 'st l [%s_]' % i
                    print 'st h [%s^]' % i
                    print 'rd l'
            else:
                print 'st l [%s_]' % variable
            print 'st h [%s^]' % variable
            if command == 'read':
                if len(args) > 1:
                    print 'rd %s' % args[0]
                else:
                    print 'rd'
            else: 
                print 'wr'

        elif command == 'copy':
            print 'cp %s' % args[0]

        elif command == 'jpz':
            print 'st h %s^' % args[0]
            print 'st l %s_' % args[0]
            print 'jz'

        elif command in alu:
            print 'al %s' % command
        
        elif command.startswith(';'):
            print command

        else:
            print 'Unknown command: %s' % command
            exit(1)
    except:
        print 'Error: %s' % line
        exit(1)
