import numpy as np

T = np.array([[0.8, 0, 0.2, 0], [0.6, 0, 0, 0.4], [0, 1, 0, 0], [0, 1, 0, 0]])
p0 = np.array([1, 0, 0, 1])
prev_p = p0
p = T.dot(prev_p)
step = 0
while not np.allclose(p, prev_p):
	while not np.array_equal(p, prev_p):
		step += 1
		prev_p = p
		p = T.dot(prev_p)
		print("Step #" + str(step))
		print(p)
		print("\n")
		if step > 10000:
			break