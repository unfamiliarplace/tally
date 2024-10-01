ANON = '--'

names = {} # TODO unused
choices = {}

print('TALLY')
print('Enter choices one by one. Blank to quit')
print('Lines with : will be interpreted as name : choice')
print()

choice = input('Next: ').strip().lower()
while choice != '':
    if ':' in choice:
        name, choice = (s.strip() for s in choice.split(':'))
    else:
        name = ANON
    
    names[name] = names.get(name, []) + [choice]
    choices[choice] = choices.get(choice, []) + [name]

    choice = input('Next: ').strip().lower()

print()
print('Results')
print('=======')
print()

longest_choice = len(max(choices, key=len))
longest_tally = len(str(len(max(choices.values(), key=len))))

for choice in sorted(choices, key=lambda c: (len(choices[c]), tuple(-ord(m) for m in c.lower())), reverse=True):
    choosers = choices[choice]
    non_anon = sorted(list(filter(lambda c: c != ANON, choosers)))
    print(f'{choice.ljust(longest_choice)} : {str(len(choosers)).rjust(longest_tally)}', end='')
    if non_anon:
        print(f' > {", ".join(non_anon)}')
    else:
        print()
