+++
title       = 'Ellipsoidal and Cartesian Coordinates Conversion'
date        = '2026-07-06T00:00:00+07:00'
draft       = false
description = 'Beginner-friendly derivation of ECEF and ellipsoidal coordinate conversion.'
tags        = ['GNSS', 'Coordinates', 'Geodesy', 'Math']
math        = true
+++

## Goal

This note explains how to convert between Earth-Centered Earth-Fixed Cartesian coordinates \((x, y, z)\) and ellipsoidal coordinates \((\varphi, \lambda, h)\). Cartesian coordinates use three straight axes from Earth's center. Ellipsoidal coordinates use latitude, longitude, and height above a reference ellipsoid.

The key point is that Earth is not modeled as a perfect sphere. It is modeled as a slightly flattened ellipsoid. We will start from the ellipse equation, derive the needed radius \(N\), then use it to get the final conversion equations.

## Geometry

The ECEF system has its origin at Earth's center. The \(z\)-axis points to the north pole, the \(x\)-axis lies on the equator at longitude \(0^\circ\), and the \(y\)-axis lies on the equator at longitude \(90^\circ\) east.

The ellipsoidal system uses geodetic latitude \(\varphi\), longitude \(\lambda\), and height \(h\). Geodetic latitude is important: it is not the angle from Earth's center. It is the angle made by the normal line of the ellipsoid. The normal line is perpendicular to the ellipsoid surface.

## Symbols

| Symbol | Meaning |
|---|---|
| \(a\) | Semi-major axis. This is the equator radius. |
| \(b\) | Semi-minor axis. This is the pole radius. |
| \(f\) | Flattening factor. |
| \(e\) | First eccentricity. It measures how far the ellipsoid is from a sphere. |
| \(\varphi\) | Geodetic latitude. |
| \(\lambda\) | Longitude. |
| \(h\) | Height along the normal line. |
| \(N\) | Radius of curvature in the prime vertical. |
| \(p\) | Horizontal distance from the \(z\)-axis. |

All angles must use the same unit. Most programs use radians. The horizontal distance from the \(z\)-axis is:

\[
p = \sqrt{x^2 + y^2}
\]

This value lets us reduce the 3D problem to a 2D problem in a meridian plane. A meridian plane is a vertical slice through the ellipsoid and the \(z\)-axis.

## The Ellipsoid

In a meridian plane, the ellipsoid becomes an ellipse. The horizontal coordinate is \(p\), and the vertical coordinate is \(z\):

\[
\frac{p^2}{a^2} + \frac{z^2}{b^2} = 1
\]

The semi-major axis \(a\) is the equator radius, and the semi-minor axis \(b\) is the pole radius. The flattening \(f\) tells us how much shorter \(b\) is than \(a\):

\[
f = 1 - \frac{b}{a}
\]

Solving the flattening equation for \(b\) gives:

\[
b = a(1 - f)
\]

The first eccentricity \(e\) is another way to measure the same flattening. It is defined by:

\[
e^2 = \frac{a^2 - b^2}{a^2}
\]

Substitute \(b = a(1 - f)\) into the definition:

\[
\begin{aligned}
e^2
&= \frac{a^2 - a^2(1-f)^2}{a^2} \\
&= 1 - (1-f)^2 \\
&= 1 - (1 - 2f + f^2) \\
&= 2f - f^2
\end{aligned}
\]

This gives the eccentricity equation used by Navipedia:

\[
e^2 = \frac{a^2 - b^2}{a^2} = 2f - f^2
\]

## Why \(N\) Appears

To derive the conversion formulas, first study a point on the ellipsoid surface, where \(h = 0\). Let the point in the meridian plane be \((p_0, z_0)\). Because this point is on the ellipse, it satisfies:

\[
\frac{p_0^2}{a^2} + \frac{z_0^2}{b^2} = 1
\]

The tangent line touches the ellipse at this point. The normal line is perpendicular to that tangent line. To find the tangent slope, differentiate the ellipse equation with respect to \(p\):

\[
\frac{2p_0}{a^2} + \frac{2z_0}{b^2}\frac{dz}{dp} = 0
\]

Solving this for the tangent slope gives:

\[
\frac{dz}{dp} = -\frac{b^2p_0}{a^2z_0}
\]

Two perpendicular lines have slopes whose product is \(-1\). Therefore the normal slope is:

\[
m_{\text{normal}} = \frac{a^2z_0}{b^2p_0}
\]

Geodetic latitude \(\varphi\) is the angle of this normal line above the equator plane. Since slope is rise over run, we have:

\[
\tan\varphi = m_{\text{normal}} = \frac{a^2z_0}{b^2p_0}
\]

Now solve for \(z_0\). Because \(1-e^2 = b^2/a^2\), the equation becomes:

\[
z_0 = \frac{b^2}{a^2}p_0\tan\varphi
\]

\[
1 - e^2 = \frac{b^2}{a^2}
\]

\[
z_0 = (1-e^2)p_0\tan\varphi
\]

Now define \(N\) through the horizontal coordinate of the surface point:

\[
p_0 = N\cos\varphi
\]

Substitute this into the \(z_0\) equation:

\[
\begin{aligned}
z_0
&= (1-e^2)N\cos\varphi\tan\varphi \\
&= (1-e^2)N\sin\varphi
\end{aligned}
\]

So the surface point can be written in terms of \(N\) and \(\varphi\):

\[
\begin{aligned}
p_0 &= N\cos\varphi \\
z_0 &= (1-e^2)N\sin\varphi
\end{aligned}
\]

To find \(N\), substitute these two expressions back into the ellipse equation:

\[
\frac{(N\cos\varphi)^2}{a^2} + \frac{\left((1-e^2)N\sin\varphi\right)^2}{b^2} = 1
\]

Since \(b^2 = a^2(1-e^2)\), the second term simplifies:

\[
\frac{(1-e^2)^2N^2\sin^2\varphi}{a^2(1-e^2)} = \frac{(1-e^2)N^2\sin^2\varphi}{a^2}
\]

After collecting terms, we get:

\[
\frac{N^2}{a^2}\left(\cos^2\varphi + (1-e^2)\sin^2\varphi\right) = 1
\]

Use the identity \(\cos^2\varphi + \sin^2\varphi = 1\):

\[
\cos^2\varphi + (1-e^2)\sin^2\varphi = 1 - e^2\sin^2\varphi
\]

Then the equation becomes:

\[
\frac{N^2}{a^2}\left(1 - e^2\sin^2\varphi\right) = 1
\]

Solving for \(N\) gives the Navipedia formula:

\[
N^2 = \frac{a^2}{1 - e^2\sin^2\varphi}
\]

\[
N =
\frac{a}{\sqrt{1 - e^2\sin^2\varphi}}
\]

This proves the Navipedia formula for \(N\).

## Ellipsoidal to Cartesian

The forward conversion starts from the surface point. From the previous section:

\[
\begin{aligned}
p_0 &= N\cos\varphi \\
z_0 &= (1-e^2)N\sin\varphi
\end{aligned}
\]

Height \(h\) is measured along the normal line, not straight away from Earth's center. In the meridian plane, the unit direction of this normal line is:

\[
(\cos\varphi, \sin\varphi)
\]

Therefore height adds \(h\cos\varphi\) to the horizontal coordinate and \(h\sin\varphi\) to the vertical coordinate:

\[
\begin{aligned}
\Delta p &= h\cos\varphi \\
\Delta z &= h\sin\varphi
\end{aligned}
\]

\[
\begin{aligned}
p &= p_0 + h\cos\varphi \\
z &= z_0 + h\sin\varphi
\end{aligned}
\]

Substitute the surface values \(p_0\) and \(z_0\):

\[
\begin{aligned}
p &= (N+h)\cos\varphi \\
z &= \left((1-e^2)N+h\right)\sin\varphi
\end{aligned}
\]

Longitude \(\lambda\) then rotates this horizontal distance into the \(x\)-\(y\) plane:

\[
\begin{aligned}
x &= p\cos\lambda \\
y &= p\sin\lambda
\end{aligned}
\]

Substitute \(p = (N+h)\cos\varphi\) to get the final forward equations:

\[
\begin{aligned}
x &= (N+h)\cos\varphi\cos\lambda \\
y &= (N+h)\cos\varphi\sin\lambda \\
z &= \left((1-e^2)N+h\right)\sin\varphi
\end{aligned}
\]

These are the final equations for converting ellipsoidal coordinates to Cartesian coordinates.

## Cartesian to Ellipsoidal

For the reverse conversion, start with \((x, y, z)\). First compute the horizontal distance from the \(z\)-axis:

\[
p = \sqrt{x^2 + y^2}
\]

Longitude is the angle in the \(x\)-\(y\) plane:

\[
\lambda = \operatorname{atan2}(y, x)
\]

The \(\operatorname{atan2}\) function is better than a plain arctangent because it uses the signs of \(x\) and \(y\). This gives the correct quadrant.

Latitude is harder because \(N\) depends on \(\varphi\), and \(\varphi\) is the value we want to find. Navipedia handles this with iteration: start with a good guess, compute \(N\) and \(h\), improve \(\varphi\), and repeat.

### Initial Latitude

If the point is near the ellipsoid surface, then \(h \approx 0\). Using the forward equations with \(h = 0\), we get:

\[
\begin{aligned}
p &= N\cos\varphi \\
z &= (1-e^2)N\sin\varphi
\end{aligned}
\]

Divide \(z\) by \(p\), then use \(\tan\varphi = \sin\varphi/\cos\varphi\):

\[
\frac{z}{p} = (1-e^2)\frac{\sin\varphi}{\cos\varphi}
\]

\[
\frac{z}{p} = (1-e^2)\tan\varphi
\]

\[
\tan\varphi = \frac{z}{(1-e^2)p}
\]

This gives the first latitude estimate:

\[
\varphi_{0} = \arctan\left(\frac{z}{(1-e^2)p}\right)
\]

This is only a starting value. The next steps improve it.

### Iteration Equations

Assume we already have a latitude estimate \(\varphi_{i-1}\). Use it to compute the matching value of \(N\):

\[
N_i =
\frac{a}{\sqrt{1-e^2\sin^2\varphi_{i-1}}}
\]

From the forward equation \(p = (N+h)\cos\varphi\), solve for \(h\):

\[
p = (N+h)\cos\varphi
\]

\[
h = \frac{p}{\cos\varphi} - N
\]

Using the current estimate, this becomes:

\[
h_i =
\frac{p}{\cos\varphi_{i-1}} - N_i
\]

Next derive the improved latitude equation from the forward \(z\) equation:

\[
z = \left((1-e^2)N+h\right)\sin\varphi
\]

Rewrite the part inside parentheses so that \(N+h\) appears:

\[
(1-e^2)N+h = N+h-e^2N
\]

\[
N+h-e^2N = (N+h)\left(1-\frac{e^2N}{N+h}\right)
\]

This changes the \(z\) equation into:

\[
z = (N+h)\left(1-\frac{e^2N}{N+h}\right)\sin\varphi
\]

Divide this by \(p = (N+h)\cos\varphi\):

\[
p = (N+h)\cos\varphi
\]

\[
\frac{z}{p} = \left(1-\frac{e^2N}{N+h}\right)\frac{\sin\varphi}{\cos\varphi}
\]

\[
\frac{z}{p} = \left(1-\frac{e^2N}{N+h}\right)\tan\varphi
\]

\[
\tan\varphi = \frac{z}{\left(1-\frac{e^2N}{N+h}\right)p}
\]

Replace \(N\) and \(h\) with the current estimates \(N_i\) and \(h_i\). The improved latitude estimate is:

\[
\varphi_i =
\arctan\left(\frac{z}{\left(1-\frac{e^2N_i}{N_i+h_i}\right)p}\right)
\]

Repeat this process until the latitude change is smaller than the precision you need:

\[
|\varphi_i - \varphi_{i-1}|
\]

## Complete Formula Set

For ellipsoidal to Cartesian conversion, given \((\varphi, \lambda, h)\), first compute \(N\), then use it in the three Cartesian equations:

\[
N =
\frac{a}{\sqrt{1-e^2\sin^2\varphi}}
\]

\[
\begin{aligned}
x &= (N+h)\cos\varphi\cos\lambda \\
y &= (N+h)\cos\varphi\sin\lambda \\
z &= \left((1-e^2)N+h\right)\sin\varphi
\end{aligned}
\]

For Cartesian to ellipsoidal conversion, given \((x, y, z)\), compute:

\[
p = \sqrt{x^2+y^2}
\]

\[
\lambda = \operatorname{atan2}(y,x)
\]

Start the iteration with:

\[
\varphi_0 =
\arctan
\left(
\frac{z}{(1-e^2)p}
\right)
\]

Repeat these update equations:

\[
\begin{aligned}
N_i &=
\frac{a}{\sqrt{1-e^2\sin^2\varphi_{i-1}}} \\
h_i &=
\frac{p}{\cos\varphi_{i-1}} - N_i \\
\varphi_i &=
\arctan\left(\frac{z}{\left(1-\frac{e^2N_i}{N_i+h_i}\right)p}\right)
\end{aligned}
\]

Stop when the latitude change is small enough.

## Simple Checks

### Perfect Sphere

If the ellipsoid is a sphere, then \(e = 0\), so \(N = a\). The forward equations reduce to the normal spherical coordinate equations:

\[
\begin{aligned}
e &= 0 \\
N &= a
\end{aligned}
\]

\[
\begin{aligned}
x &= (a+h)\cos\varphi\cos\lambda \\
y &= (a+h)\cos\varphi\sin\lambda \\
z &= (a+h)\sin\varphi
\end{aligned}
\]

This is a good sanity check because the ellipsoid model becomes the sphere model when there is no flattening.

### Equator

At the equator, \(\varphi = 0\). Therefore \(\sin\varphi = 0\) and \(\cos\varphi = 1\). For \(h = 0\), the point is on the equator:

\[
\varphi = 0
\]

\[
\sin\varphi = 0
\]

\[
\cos\varphi = 1
\]

\[
\begin{aligned}
x &= a\cos\lambda \\
y &= a\sin\lambda \\
z &= 0
\end{aligned}
\]

This matches the expected equator radius.

### North Pole

At the north pole, \(\varphi = 90^\circ\). For \(h = 0\), the horizontal coordinates are zero and the vertical coordinate is \(b\):

\[
\varphi = 90^\circ
\]

\[
\begin{aligned}
x &= 0 \\
y &= 0 \\
z &= b
\end{aligned}
\]

This means the point lies at the top of the ellipsoid, as expected.

## Practical Notes

- Use the same ellipsoid constants as the coordinate frame.
- WGS 84 is common for GNSS work.
- Use \(\operatorname{atan2}(y,x)\), not only \(\arctan(y/x)\).
- Near the poles, \(p = 0\), so longitude is not well-defined.
- If \(p = 0\), a common choice is to keep a previous longitude or set \(\lambda = 0\).
- At the poles, latitude is \(\pm 90^\circ\), and height is approximately \(|z| - b\).
- The iteration usually converges quickly because Earth is close to a sphere.

## References

- [Navipedia: Ellipsoidal and Cartesian Coordinates Conversion](https://gssc.esa.int/navipedia/index.php/Ellipsoidal_and_Cartesian_Coordinates_Conversion)
