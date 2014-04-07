#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) < 2:
    print 'Usage: python %s <inputfile>' % sys.argv[0]
    exit(1)

inputfile = open(sys.argv[1]).read()

def get_value(x):
    if x.startswith('0x'):
        return int(x, 16)
    elif x.startswith('0b'):
        return int(x, 2)
    return int(x)

def is_value(x):
    try:
        get_value(x)
        return True
    except ValueError:
        return False

def get_indentation_from_line(line):
    return line[:-len(line.lstrip(' '))]

def find_end_of_block(lines, start):
    i = start
    base_indentation = get_indentation_from_line(lines[start])
    while i < len(lines) - 1:
        i += 1
        this = get_indentation_from_line(lines[i])
        if not this.startswith(base_indentation):
            return i
        elif this == base_indentation:
            return i
    return len(lines)

def do_calculation(line, operator, code_name, swap=False):
    left, right = line.split(operator)
    if swap:
        left, right = right, left
    right = right.strip(' ')
    left = left.strip(' ')
    if is_value(right):
        print 'set c %s' % right
    elif right == '@':
        print 'cp c'
    else:
        print 'read c %s' % right
    if is_value(left):
        print 'set b %s' % left
    elif left == '@':
        print 'cp b'
    else:
        print 'read b %s' % left
    print code_name

def parse_code(lines):
    i = 0
    last_comment = ''
    while i < len(lines):
        line = lines[i]
        #print '>',line

        if not line.split('//')[0].split():
            print line.strip(' ')
        
        if '//' in line:
            if line.strip(' ').startswith('//'):
            #    print line
                last_comment = line.split('//', 1)[1].strip(' ')
            line = line[:line.find('//')]
        
        if not line.split():
            i += 1
            continue
    
        if line.split()[0] == 'loop':
            print ';%s_loop' % last_comment.replace(' ', '_')
            j = find_end_of_block(lines, i)
            parse_code(lines[i+1 : j])
            print 'jpz ;%s_loop' % last_comment.replace(' ', '_')
            i = j - 1

        elif line.split()[0] == 'if':
            parse_code([line.split('if', 1)[1].strip(' ')])
            print 'jpz ;no_%s' % last_comment.replace(' ', '_')
            j = find_end_of_block(lines, i)
            parse_code(lines[i+1 : j])
            print ';no_%s' % last_comment.replace(' ', '_')
            i = j - 1
    
        # value -> variable
        elif ':=' in line:
            left, right = line.split(':=')
            right = right.strip(' ')
            left = left.strip(' ')
            if is_value(right):
                print 'set %s' % right
            elif right == '@':
                pass
            else:
                print 'read %s' % right

            for variable in left.split(','):
                print 'write %s' % variable.strip(' ')
        
        # +=
        elif '+=' in line:
            left, right = line.split('+=')
            right = right.strip(' ')
            left = left.strip(' ')
            print 'read b %s' % left
            if is_value(right):
                print 'set c %s' % right
            elif right == '@':
                print 'cp c'
            else:
                print 'read c %s' % right
            print 'add'
            print 'write %s' % left
        
        # -=
        elif '-=' in line:
            left, right = line.split('-=')
            right = right.strip(' ')
            left = left.strip(' ')
            if is_value(right):
                if right[0] == '-':
                    print 'set c %s' % right[1:]
                else:
                    print 'set c -%s' % right
            elif right == '@':
                print 'cp c'
                print 'set b -1'
                print 'mul'
                print 'cp c'
            else:
                print 'read c %s' % right
                print 'set b -1'
                print 'mul'
                print 'cp c'
            print 'read b %s' % left
            print 'add'
            print 'write %s' % left
        
        elif '-' in line:
            left, right = line.split('-')
            right = right.strip(' ')
            left = left.strip(' ')
            if is_value(right):
                if right[0] == '-':
                    print 'set c %s' % right[1:]
                else:
                    print 'set c -%s' % right
            elif right == '@':
                print 'cp c'
                print 'set b -1'
                print 'mul'
                print 'cp c'
            else:
                print 'read c %s' % right
                print 'set b -1'
                print 'mul'
                print 'cp c'
            if is_value(left):
                print 'set b %s' % left
            elif left == '@':
                print 'cp b'
            else:
                print 'read b %s' % left
            print 'add'

        elif '/' in line:
            do_calculation(line, '/', 'div')
        
        elif '<' in line:
            do_calculation(line, '<', 'div')
        
        elif '>' in line:
            do_calculation(line, '>', 'div', True)
        
        elif '+' in line:
            do_calculation(line, '+', 'add')
        
        elif '%' in line:
            do_calculation(line, '%', 'mod')
        
        elif '*' in line:
            do_calculation(line, '*', 'mul')
        
        elif 'or' in line:
            do_calculation(line, 'or', 'or')
        
        elif line.split()[0] in ['read', 'write', 'jpz', 'set']:
            print line.strip(' ')

        elif line.strip(' ')[0] == '>':
            print line.strip(' ')[1:]

        elif line.strip(' ')[0] == ';':
            print line.strip(' ')

        else:
            print 'Syntax error: %s' % line
            exit(1)
        i += 1

parse_code(inputfile.split('\n')[:-1])
