import string,random
length=7
final=""
char=string.digits+string.ascii_uppercase+string.ascii_lowercase
for _ in range(length):
    final+=random.choice(char)
print final