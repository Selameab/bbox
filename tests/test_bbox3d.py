from bbox import BBox3D
from bbox.utils import draw_cuboid

import numpy as np
from PIL import Image, ImageDraw
import pytest


class TestBBox3d:
    @classmethod
    def setup_class(cls):
        # sample cuboid
        cuboid = {
            'center': {
                'x': -49.19743041908411,
                'y': 12.38666074615689,
                'z': 0.782056864653507
            },
            'dimensions': {
                'length': 5.340892485711914,
                'width': 2.457703972075464,
                'height': 1.9422248281533563
            },
            'rotation': {
                'w': 0.9997472337219893,
                'x': 0.0,
                'y': 0.0,
                'z': 0.022482630300529462
            }
        }
        center = cuboid['center']
        dim = cuboid['dimensions']
        rotation = cuboid['rotation']

        cls.box = BBox3D(center['x'], center['y'], center['z'],
                         length=dim['length'], width=dim['width'], height=dim['height'],
                         rw=rotation['w'], rx=rotation['x'], ry=rotation['y'], rz=rotation['z'])
        cls.cuboid = cuboid

    def test_points(self):
        points = np.array([[-51.80993533, 11.03900409,  -0.18905555],
                           [-46.47444215, 11.27909801,  -0.18905555],
                           [-46.58492551, 13.7343174,   -0.18905555],
                           [-51.92041869, 13.49422348,  -0.18905555],
                           [-51.80993533, 11.03900409,  1.75316928],
                           [-46.47444215, 11.27909801,  1.75316928],
                           [-46.58492551, 13.7343174,   1.75316928],
                           [-51.92041869, 13.49422348,  1.75316928]])

        assert np.allclose(self.box.p1[0: 3], points[0, :])
        assert np.allclose(self.box.p2[0: 3], points[1, :])
        assert np.allclose(self.box.p3[0: 3], points[2, :])
        assert np.allclose(self.box.p4[0: 3], points[3, :])
        assert np.allclose(self.box.p5[0: 3], points[4, :])
        assert np.allclose(self.box.p6[0: 3], points[5, :])
        assert np.allclose(self.box.p7[0: 3], points[6, :])
        assert np.allclose(self.box.p8[0: 3], points[7, :])

        assert np.allclose(self.box.p[:, 0:3], points)

    def test_center(self):
        center = np.array(
            [-49.19743041908411, 12.38666074615689, 0.782056864653507])
        # we get homogenous coordinates
        assert np.array_equal(self.box.center[0:3], center)

    def test_center_points(self):
        assert self.box.cx == self.cuboid['center']['x']
        assert self.box.cy == self.cuboid['center']['y']
        assert self.box.cz == self.cuboid['center']['z']

    def test_quaternion(self):
        q = np.array([0.9997472337219893, 0.0, 0.0, 0.022482630300529462])
        assert np.array_equal(self.box.q, q)
        # alternative attribute for the quaternion
        assert np.array_equal(self.box.quaternion, q)

    def test_euler_angles(self):
        box = BBox3D(3.163, z=2.468, y=34.677, height=1.529, width=1.587, length=3.948,
                     euler_angles=[0, 0, -1.59])
        q = np.array([0.7002847660410397, -0.0, -0.0, -0.7138636049350369])
        assert np.array_equal(box.q, q)

    def test_projection(self):
        K = np.array([[1406.3359, 0.0, 966.366034, 0.0],
                      [0.0, 1408.94297, 607.479746, 0.0],
                      [0.0, 0.0, 1.0, 0.0]])

        R = np.array([[0.50478576,  0.86323317, -0.00445338],
                      [-0.00422247, -0.00268975, -0.99998747],
                      [-0.86323433,  0.50479824,  0.00228723]])

        t = np.array([[-0.75116634], [1.35776453], [0.87137971]])

        u = np.empty((8, 2))
        u[0] = self.project(self.box.p1, K, R, t)
        u[1] = self.project(self.box.p2, K, R, t)
        u[2] = self.project(self.box.p3, K, R, t)
        u[3] = self.project(self.box.p4, K, R, t)
        u[4] = self.project(self.box.p5, K, R, t)
        u[5] = self.project(self.box.p6, K, R, t)
        u[6] = self.project(self.box.p7, K, R, t)
        u[7] = self.project(self.box.p8, K, R, t)

        image_points = np.array([[488.84269983, 655.2790429],
                                 [530.3490365,  659.17142666],
                                 [602.90920984, 657.55445187],
                                 [556.26022377, 653.89914093],
                                 [488.64644505, 601.79933826],
                                 [530.12998103, 600.55433066],
                                 [602.68953074, 600.56675254],
                                 [556.06325411, 601.7790501]])

        for i in range(8):
            assert np.allclose(u[i], image_points[i])

    @pytest.mark.skip(reason="This is just for visualization. We already test the values beforehand.")
    def test_render(self):
        K = np.array([[1406.3359, 0.0, 966.366034, 0.0],
                      [0.0, 1408.94297, 607.479746, 0.0],
                      [0.0, 0.0, 1.0, 0.0]])

        R = np.array([[0.50478576,  0.86323317, -0.00445338],
                      [-0.00422247, -0.00268975, -0.99998747],
                      [-0.86323433,  0.50479824,  0.00228723]])

        t = np.array([[-0.75116634], [1.35776453], [0.87137971]])

        u = np.empty((8, 2))
        u[0] = self.project(self.box.p1, K, R, t)
        u[1] = self.project(self.box.p2, K, R, t)
        u[2] = self.project(self.box.p3, K, R, t)
        u[3] = self.project(self.box.p4, K, R, t)
        u[4] = self.project(self.box.p5, K, R, t)
        u[5] = self.project(self.box.p6, K, R, t)
        u[6] = self.project(self.box.p7, K, R, t)
        u[7] = self.project(self.box.p8, K, R, t)

        img = Image.open("image_raw_ring_rear_left_315968023469083760.png")

        dist_coeff = [-0.17120984449230167,
                      0.1256910189977147,
                      -0.029726711792577232]

        for i in range(u.shape[0]):
            u[i] = self.distortion_correction(u[i], dist_coeff, img.size)

        img = draw_cuboid(img, u)
        img.show()

    @staticmethod
    def project(p, K, R, t):
        E = np.eye(4)
        E[0: 3, 0: 3] = R
        E[0: 3, 3: 4] = t

        u = K @ E @ p
        # print("projection", u)
        return u[0: 2] / u[2]

    @staticmethod
    def distortion_correction(u, dist_coeff, img_size):
        w, h = img_size
        # normalize the image coords
        x = 2*u[0]/w - 1
        y = 2*u[1]/h - 1
        r = np.linalg.norm(np.array(x, y))

        r2 = r**2

        distortion = 0
        for i in range(len(dist_coeff)):
            distortion += ((r2**(i+1)) * dist_coeff[i])

        # correct for distortion
        v = u + (u - np.array([w, h])/2)*distortion
        return v
