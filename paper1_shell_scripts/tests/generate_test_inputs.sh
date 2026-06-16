#!/bin/bash
# generate_test_inputs.sh -- create all test inputs for Paper 1 benchmarks

echo "Generating test inputs..."
python3 -c "
import random, string
lines = []
for i in range(5000):
    r = random.random()
    if r < 0.3:
        lines.append('> Quoted line %d: ' % i + ' '.join(['word']*random.randint(5,20)))
    elif r < 0.5:
        lines.append('   > Indented quote %d: ' % i + ' '.join(['word']*random.randint(5,15)))
    else:
        lines.append('Plain line %d: ' % i + ' '.join(['word']*random.randint(10,30)))
open('test_email.txt','w').write('
'.join(lines))
print('Generated test_email.txt (5000 lines)')
"
echo -e "Alice
Bob
Charlie
Diana
Evan" > names
printf 'Dear NAME,

Your application reference is REF-NAME-2026.

Best regards,
The Team
' > template.txt
echo "Generated names and template.txt"

mkdir -p test_spaces
for i in $(seq 1 50); do touch "test_spaces/file $i.txt"; done
for i in $(seq 1 50); do touch "test_spaces/no_space_$i.txt"; done
echo "Generated test_spaces/ (50 files with spaces, 50 without)"
echo "Done."
