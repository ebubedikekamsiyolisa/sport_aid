import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize = (8,5))
ax.plot([1,2,3,4],[10,20,15, 30, 39], marker = 'o', color='red')
ax.set_title("Quaterly Revenue")
ax.set_xlabel('Quater')
ax.set_ylabel('Revenue')
plt.show()
