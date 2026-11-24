m = 20.0
p = [24.0, 15.0, 25.0]
w = [15.0, 10.0, 18.0]
x = p.length

i = 0
for (int(i) < x.length):
    x[i] = 0.0
    i += 1

float(capacity) = m


i = 0
for (int(i) < x.length):
    i += 1
    
    if (int(i) < (x.length - 1)):
        x[i] = capacity / w[i]    

    if (w[i] > capacity):
        break

    else:
        x[i] = 1.0;
        float(capacity) -= w[i]

print("Fractional Solution:")

for (float(value) : x):
    print(value)

