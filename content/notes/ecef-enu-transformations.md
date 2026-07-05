+++
title       = 'Transformations Between ECEF and ENU Coordinates'
date        = '2026-07-06T00:00:00+07:00'
draft       = false
description = 'Beginner-friendly derivation of ECEF and ENU coordinate transformations.'
tags        = ['GNSS', 'Coordinate Systems', 'Math']
math        = true
+++

## Goal

This note explains the Navipedia page about transformations between ECEF and ENU coordinates. The goal is to understand how a local vector written as East, North, and Up can be written in the global Earth-Centered Earth-Fixed frame. The final ENU-to-ECEF equation is:

\[\begin{bmatrix}x\\y\\z\end{bmatrix} = \begin{bmatrix} -\sin\lambda & -\cos\lambda\sin\varphi & \cos\lambda\cos\varphi\\ \cos\lambda & -\sin\lambda\sin\varphi & \sin\lambda\cos\varphi\\ 0 & \cos\varphi & \sin\varphi \end{bmatrix} \begin{bmatrix}E\\N\\U\end{bmatrix}\]

The inverse equation converts an ECEF vector back to the local ENU frame:

\[\begin{bmatrix}E\\N\\U\end{bmatrix} = \begin{bmatrix} -\sin\lambda & \cos\lambda & 0\\ -\cos\lambda\sin\varphi & -\sin\lambda\sin\varphi & \cos\varphi\\ \cos\lambda\cos\varphi & \sin\lambda\cos\varphi & \sin\varphi \end{bmatrix} \begin{bmatrix}x\\y\\z\end{bmatrix}\]

Here, \(\lambda\) is longitude, \(\varphi\) is latitude, and \(E,N,U\) mean East, North, and Up. The values \(x,y,z\) are components in the ECEF frame.

## ECEF And ENU

ECEF means Earth-Centered Earth-Fixed. Its origin is at the center of Earth, and its axes rotate with Earth. The \(x\)-axis points to longitude \(0^\circ\), latitude \(0^\circ\). The \(y\)-axis points to longitude \(90^\circ\) East, latitude \(0^\circ\). The \(z\)-axis points to the North Pole.

ENU is different because it is a local frame. It is built at one chosen point, for example a GNSS receiver. East is tangent to Earth and points toward larger longitude. North is tangent to Earth and points toward larger latitude. Up is normal to the local tangent plane. If the latitude and longitude are geodetic coordinates on an ellipsoid, Up is normal to the ellipsoid. If they are spherical coordinates, Up is radial from the Earth center.

## Vector Or Position

The matrix above converts vectors, not absolute positions. This is important because ENU is local at one receiver point. To convert the position of a target point into ENU, first subtract the receiver position.

Let the receiver ECEF position be:

\[\mathbf r_0 = \begin{bmatrix}x_0\\y_0\\z_0\end{bmatrix}\]

Let the target ECEF position be:

\[\mathbf r = \begin{bmatrix}x\\y\\z\end{bmatrix}\]

The vector from the receiver to the target is:

\[\Delta\mathbf r = \mathbf r - \mathbf r_0\]

Then the local ENU vector is:

\[\begin{bmatrix}E\\N\\U\end{bmatrix} = \mathbf M^T \Delta\mathbf r\]

So, do not apply the ECEF-to-ENU matrix to a raw ECEF position unless you really mean a vector from the Earth center.

## Build The Local Unit Vectors

The easiest way to understand the matrix is to build the three local unit vectors: East, North, and Up. A unit vector has length \(1\). We will write each local unit vector using ECEF components, then place those vectors into a matrix.

### Horizontal Direction

First look at the receiver from above the North Pole. The horizontal direction from the Earth center to longitude \(\lambda\) lies in the ECEF \(xy\)-plane, so it is:

\[\hat{\mathbf h} = \begin{bmatrix} \cos\lambda\\ \sin\lambda\\ 0 \end{bmatrix}\]

This is a unit vector because:

\[\cos^2\lambda + \sin^2\lambda = 1\]

### Up Vector

Latitude \(\varphi\) tells how far the Up direction rises above the equator. The horizontal part of Up has length \(\cos\varphi\), and the vertical \(z\)-part has length \(\sin\varphi\). Therefore:

\[\hat{\mathbf u} = \cos\varphi \hat{\mathbf h} + \sin\varphi \begin{bmatrix}0\\0\\1\end{bmatrix}\]

Putting in \(\hat{\mathbf h}\) gives:

\[\hat{\mathbf u} = \begin{bmatrix} \cos\lambda\cos\varphi\\ \sin\lambda\cos\varphi\\ \sin\varphi \end{bmatrix}\]

This vector becomes the third column of the ENU-to-ECEF matrix because it is the ECEF direction of local Up.

### East Vector

East means the direction of increasing longitude. In the \(xy\)-plane, it is a \(90^\circ\) turn from the horizontal direction:

\[\begin{bmatrix}\cos\lambda\\\sin\lambda\\0\end{bmatrix}\]

After the turn, the East unit vector is:

\[\hat{\mathbf e} = \begin{bmatrix} -\sin\lambda\\ \cos\lambda\\ 0 \end{bmatrix}\]

This direction check is useful. At \(\lambda=0^\circ\), which is Greenwich on the equator, \(x\) points Up and East points toward \(+y\). The formula gives:

\[\hat{\mathbf e} = \begin{bmatrix}0\\1\\0\end{bmatrix}\]

That matches the expected direction.

### North Vector

North means increasing latitude. In the meridian plane, North is perpendicular to Up. It has horizontal part \(-\sin\varphi\) and vertical part \(\cos\varphi\), so:

\[\hat{\mathbf n} = -\sin\varphi \hat{\mathbf h} + \cos\varphi \begin{bmatrix}0\\0\\1\end{bmatrix}\]

Putting in \(\hat{\mathbf h}\) gives:

\[\hat{\mathbf n} = \begin{bmatrix} -\cos\lambda\sin\varphi\\ -\sin\lambda\sin\varphi\\ \cos\varphi \end{bmatrix}\]

This vector becomes the second column of the ENU-to-ECEF matrix because it is the ECEF direction of local North.

## Prove The Axes Are Valid

The three local axes must have length \(1\), and they must be perpendicular to each other. The East vector has length \(1\) because:

\[(-\sin\lambda)^2 + (\cos\lambda)^2 + 0^2 = 1\]

The Up vector also has length \(1\):

\[\cos^2\varphi(\cos^2\lambda+\sin^2\lambda)+\sin^2\varphi=1\]

The North vector has length \(1\) for the same reason:

\[\sin^2\varphi(\cos^2\lambda+\sin^2\lambda)+\cos^2\varphi=1\]

Now use dot products to prove the axes are perpendicular. East and Up have dot product:

\[\hat{\mathbf e}\cdot\hat{\mathbf u} = (-\sin\lambda)(\cos\lambda\cos\varphi) + (\cos\lambda)(\sin\lambda\cos\varphi) =0\]

East and North also have dot product zero:

\[\hat{\mathbf e}\cdot\hat{\mathbf n} = (-\sin\lambda)(-\cos\lambda\sin\varphi) + (\cos\lambda)(-\sin\lambda\sin\varphi) =0\]

North and Up have dot product zero too:

\[\hat{\mathbf n}\cdot\hat{\mathbf u} = -\sin\varphi\cos\varphi(\cos^2\lambda+\sin^2\lambda) + \sin\varphi\cos\varphi =0\]

Because all three vectors have length \(1\) and are perpendicular, they form a valid 3D coordinate frame.

## Derive ENU To ECEF

A local vector written in ENU is:

\[\mathbf v_{enu} = \begin{bmatrix}E\\N\\U\end{bmatrix}\]

This means the real vector is \(E\) steps along East, \(N\) steps along North, and \(U\) steps along Up:

\[\mathbf v = E\hat{\mathbf e} + N\hat{\mathbf n} + U\hat{\mathbf u}\]

Now insert the three unit vectors:

\[\mathbf v = E \begin{bmatrix} -\sin\lambda\\ \cos\lambda\\ 0 \end{bmatrix} + N \begin{bmatrix} -\cos\lambda\sin\varphi\\ -\sin\lambda\sin\varphi\\ \cos\varphi \end{bmatrix} + U \begin{bmatrix} \cos\lambda\cos\varphi\\ \sin\lambda\cos\varphi\\ \sin\varphi \end{bmatrix}\]

Group the \(x\), \(y\), and \(z\) parts:

\[x = -E\sin\lambda -N\cos\lambda\sin\varphi +U\cos\lambda\cos\varphi\]

\[y = E\cos\lambda -N\sin\lambda\sin\varphi +U\sin\lambda\cos\varphi\]

\[z = N\cos\varphi +U\sin\varphi\]

In matrix form, this becomes:

\[\begin{bmatrix}x\\y\\z\end{bmatrix} = \mathbf M \begin{bmatrix}E\\N\\U\end{bmatrix}\]

where:

\[\mathbf M = \begin{bmatrix} -\sin\lambda & -\cos\lambda\sin\varphi & \cos\lambda\cos\varphi\\ \cos\lambda & -\sin\lambda\sin\varphi & \sin\lambda\cos\varphi\\ 0 & \cos\varphi & \sin\varphi \end{bmatrix}\]

The main idea is that the columns of \(\mathbf M\) are the ECEF forms of the local unit vectors:

\[\mathbf M = \begin{bmatrix} | & | & |\\ \hat{\mathbf e} & \hat{\mathbf n} & \hat{\mathbf u}\\ | & | & | \end{bmatrix}\]

## Derive ECEF To ENU

Because \(\hat{\mathbf e}\), \(\hat{\mathbf n}\), and \(\hat{\mathbf u}\) are unit and perpendicular, \(\mathbf M\) is an orthonormal matrix. For this kind of matrix, the inverse is the transpose:

\[\mathbf M^{-1} = \mathbf M^T\]

So the inverse transform is:

\[\begin{bmatrix}E\\N\\U\end{bmatrix} = \mathbf M^T \begin{bmatrix}x\\y\\z\end{bmatrix}\]

The transpose is:

\[\mathbf M^T = \begin{bmatrix} -\sin\lambda & \cos\lambda & 0\\ -\cos\lambda\sin\varphi & -\sin\lambda\sin\varphi & \cos\varphi\\ \cos\lambda\cos\varphi & \sin\lambda\cos\varphi & \sin\varphi \end{bmatrix}\]

This gives the scalar equations:

\[E=-x\sin\lambda+y\cos\lambda\]

\[N=-x\cos\lambda\sin\varphi-y\sin\lambda\sin\varphi+z\cos\varphi\]

\[U=x\cos\lambda\cos\varphi+y\sin\lambda\cos\varphi+z\sin\varphi\]

For a real target point, use \(\Delta x,\Delta y,\Delta z\), not raw \(x,y,z\).

## Same Result From Rotation Matrices

Navipedia also derives the matrix by two rotations. It uses these rotation matrices:

\[\mathbf R_1(\theta) = \begin{bmatrix} 1&0&0\\ 0&\cos\theta&\sin\theta\\ 0&-\sin\theta&\cos\theta \end{bmatrix}\]

\[\mathbf R_3(\theta) = \begin{bmatrix} \cos\theta&\sin\theta&0\\ -\sin\theta&\cos\theta&0\\ 0&0&1 \end{bmatrix}\]

The ENU-to-ECEF rotation is:

\[\mathbf M = \mathbf R_3\left(-\frac{\pi}{2}-\lambda\right) \mathbf R_1\left(\varphi-\frac{\pi}{2}\right)\]

Use the angle identities:

\[\cos\left(\varphi-\frac{\pi}{2}\right)=\sin\varphi\]

\[\sin\left(\varphi-\frac{\pi}{2}\right)=-\cos\varphi\]

Then:

\[\mathbf R_1\left(\varphi-\frac{\pi}{2}\right) = \begin{bmatrix} 1&0&0\\ 0&\sin\varphi&-\cos\varphi\\ 0&\cos\varphi&\sin\varphi \end{bmatrix}\]

Also use:

\[\cos\left(-\frac{\pi}{2}-\lambda\right)=-\sin\lambda\]

\[\sin\left(-\frac{\pi}{2}-\lambda\right)=-\cos\lambda\]

Then:

\[\mathbf R_3\left(-\frac{\pi}{2}-\lambda\right) = \begin{bmatrix} -\sin\lambda&-\cos\lambda&0\\ \cos\lambda&-\sin\lambda&0\\ 0&0&1 \end{bmatrix}\]

Multiplying the two matrices gives the same \(\mathbf M\):

\[\mathbf M = \begin{bmatrix} -\sin\lambda & -\cos\lambda\sin\varphi & \cos\lambda\cos\varphi\\ \cos\lambda & -\sin\lambda\sin\varphi & \sin\lambda\cos\varphi\\ 0 & \cos\varphi & \sin\varphi \end{bmatrix}\]

This proves that the unit-vector view and the rotation-matrix view match.

## Elevation And Azimuth

Suppose we know the receiver ECEF position \(\mathbf r_{rcv}\) and the satellite ECEF position \(\mathbf r_{sat}\). The line-of-sight vector is:

\[\boldsymbol\rho = \mathbf r_{sat} - \mathbf r_{rcv}\]

The unit line-of-sight vector is:

\[\hat{\boldsymbol\rho} = \frac{\boldsymbol\rho}{\|\boldsymbol\rho\|}\]

Convert it to local ENU components with:

\[\begin{bmatrix} \rho_E\\ \rho_N\\ \rho_U \end{bmatrix} = \mathbf M^T \hat{\boldsymbol\rho}\]

This is the same as taking three dot products:

\[\rho_E=\hat{\boldsymbol\rho}\cdot\hat{\mathbf e}\]

\[\rho_N=\hat{\boldsymbol\rho}\cdot\hat{\mathbf n}\]

\[\rho_U=\hat{\boldsymbol\rho}\cdot\hat{\mathbf u}\]

Elevation is the angle above the local horizon. Since the Up component is \(\rho_U = \sin(\text{elevation})\), the elevation is:

\[\text{elevation} = \arcsin(\rho_U)\]

Azimuth is measured in the local horizontal plane. It starts at North and increases toward East, so:

\[\tan(\text{azimuth}) = \frac{\rho_E}{\rho_N}\]

For computation, use the two-input arctangent:

\[\text{azimuth} = \operatorname{atan2}(\rho_E,\rho_N)\]

If the result is negative, add \(2\pi\) radians or \(360^\circ\). This avoids the quadrant problem of a normal arctangent.

## Worked Example

Use a receiver at \(\lambda=0^\circ\) and \(\varphi=0^\circ\). This point is on the equator at Greenwich, so:

\[\sin\lambda=0,\quad \cos\lambda=1,\quad \sin\varphi=0,\quad \cos\varphi=1\]

The local unit vectors become:

\[\hat{\mathbf e} = \begin{bmatrix}0\\1\\0\end{bmatrix}, \qquad \hat{\mathbf n} = \begin{bmatrix}0\\0\\1\end{bmatrix}, \qquad \hat{\mathbf u} = \begin{bmatrix}1\\0\\0\end{bmatrix}\]

This means local East is ECEF \(+y\), local North is ECEF \(+z\), and local Up is ECEF \(+x\). If a local vector is:

\[\begin{bmatrix}E\\N\\U\end{bmatrix} = \begin{bmatrix}100\\20\\5\end{bmatrix}\]

then its ECEF vector is:

\[\begin{bmatrix}x\\y\\z\end{bmatrix} = 100 \begin{bmatrix}0\\1\\0\end{bmatrix} + 20 \begin{bmatrix}0\\0\\1\end{bmatrix} + 5 \begin{bmatrix}1\\0\\0\end{bmatrix} = \begin{bmatrix}5\\100\\20\end{bmatrix}\]

This result matches the meaning of the axes.

## Common Mistakes

Use radians if your math library expects radians, and keep the angle order clear. This note uses \(\lambda\) for longitude and \(\varphi\) for latitude. Also remember to subtract the receiver position before converting an ECEF position into ENU.

Use geodetic latitude if you want Up to be normal to an ellipsoid. For azimuth, use \(\operatorname{atan2}(\rho_E,\rho_N)\), not only \(\arctan(\rho_E/\rho_N)\), because the two-input arctangent handles the correct quadrant.

## Summary

The whole transform comes from three local unit vectors:

\[\hat{\mathbf e} = \begin{bmatrix} -\sin\lambda\\ \cos\lambda\\ 0 \end{bmatrix}\]

\[\hat{\mathbf n} = \begin{bmatrix} -\cos\lambda\sin\varphi\\ -\sin\lambda\sin\varphi\\ \cos\varphi \end{bmatrix}\]

\[\hat{\mathbf u} = \begin{bmatrix} \cos\lambda\cos\varphi\\ \sin\lambda\cos\varphi\\ \sin\varphi \end{bmatrix}\]

Put these vectors as matrix columns to convert ENU to ECEF. Then transpose that matrix to convert ECEF vectors to ENU. Finally, use the ENU components of a line-of-sight vector to compute satellite elevation and azimuth.

## References

- [Transformations between ECEF and ENU coordinates, Navipedia](https://gssc.esa.int/navipedia/index.php?title=Transformations_between_ECEF_and_ENU_coordinates)
