import numpy as np

def determine_projection_data(points, tris, iters=50, restarts=6, alpha0=0.6, alpha_decay=0.985):
    """
    points: (3, N) float, sanitized finite
    tris:   (3, M) int, sanitized valid indices, nondegenerate triangles

    Goal:
      Find a unit normal n that maximizes min_i |n · n_i|,
      where n_i are triangle unit normals. (Avoid any triangle being ~orthogonal to n.)

    Returns:
      origin, u, v  each (3,)
      u,v orthogonal, equal length, defining a square that contains all projected points.
    """

    pts = np.asarray(points, dtype=np.float64)
    tri = np.asarray(tris, dtype=np.int64)

    # --- triangle unit normals (3, M)
    p0 = pts[:, tri[0]]
    p1 = pts[:, tri[1]]
    p2 = pts[:, tri[2]]
    e1 = p1 - p0
    e2 = p2 - p0
    n_raw = np.cross(e1.T, e2.T).T
    n_unit = n_raw / np.linalg.norm(n_raw, axis=0)

    # --- objective: f(n) = min_i |n·n_i|
    def score(n):
        return np.min(np.abs(np.dot(n_unit.T, n)))

    # --- start directions
    # 1) mean normal (good for mostly planar surfaces)
    n0 = n_unit[:,0]
    n0 /= np.linalg.norm(n0)

    # 2) a few random starts to escape local traps
    rng = np.random.default_rng(0)
    starts = [n0]
    for _ in range(restarts - 1):
        r = rng.normal(size=3)
        r /= np.linalg.norm(r)
        starts.append(r)

    best_n = n0
    best_s = score(best_n)

    # --- maximin ascent (nudge toward current worst-aligned normal)
    for s0 in starts:
        n = s0.copy()
        alpha = alpha0
        for _ in range(iters):
            dots = np.dot(n_unit.T, n)           # (M,)
            i = np.argmin(np.abs(dots))       # worst (most orthogonal) triangle
            target = np.sign(dots[i]) * n_unit[:, i]  # choose orientation to increase abs dot
            n = n + alpha * target
            n /= np.linalg.norm(n)
            alpha *= alpha_decay

        s = score(n)
        if s > best_s:
            best_s = s
            best_n = n

    n = best_n  # final plane normal, unit

    # --- build in-plane orthonormal basis u_hat, v_hat
    # pick a stable axis not parallel to n
    a = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(n,a)) > 0.9:
        a = np.array([0.0, 1.0, 0.0])

    u_hat = np.cross(a, n)
    u_hat /= np.linalg.norm(u_hat)
    v_hat = np.cross(n, u_hat)  # already unit, orthogonal

    # --- project points, make containing square
    centroid = pts.mean(axis=1)
    X = pts - centroid[:, None]

    cu = np.dot(u_hat, X)
    cv = np.dot(v_hat, X)

    min_u, max_u = cu.min(), cu.max()
    min_v, max_v = cv.min(), cv.max()
    range_u = max_u - min_u
    range_v = max_v - min_v

    L = max(range_u, range_v)
    pad_u = L - range_u
    pad_v = L - range_v
    min_u_sq = min_u - 0.5 * pad_u
    min_v_sq = min_v - 0.5 * pad_v

    origin = centroid + u_hat * min_u_sq + v_hat * min_v_sq
    u = u_hat * L
    v = v_hat * L

    return origin, u, v