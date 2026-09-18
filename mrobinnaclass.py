import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8,5))
ax.plot([1,2,3,4],[2,8,6,16],marker='o',color='green')
ax.set_title("Quaterly Revenue")
ax.set_xlabel("Quater")
ax.set_ylabel("Revenue")
plt.show()