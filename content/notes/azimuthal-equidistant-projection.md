+++
title       = 'Azimuthal Equidistant Projection'
date        = '2026-07-09T00:00:00+07:00'
draft       = false
description = 'Beginner-friendly explanation of the azimuthal equidistant map projection.'
tags        = ['Geodesy', 'Map Projection', 'Math']
math        = true
+++

## Goal

The Azimuthal Equidistant Projection maps points from a sphere onto a flat plane. It is called azimuthal because the map is built around one chosen center point. Directions from this center are shown correctly. It is called equidistant because distances measured from the center to any other point are preserved in scale.

This projection does not preserve area. It also does not preserve angles everywhere. Its main purpose is simple: keep the distance from the center correct. So it is useful when the main question is how far each place is from one selected location.

## Symbols

| Symbol | Meaning |
|---|---|
| \(\phi\) | Latitude of the point being projected. |
| \(\lambda\) | Longitude of the point being projected. |
| \(\phi_1\) | Latitude of the projection center. |
| \(\lambda_0\) | Longitude of the projection center. |
| \(c\) | Angular distance from the projection center to the point. |
| \(k'\) | Scale factor used in the forward formulas. |
| \(x\) | Horizontal coordinate on the flat map. |
| \(y\) | Vertical coordinate on the flat map. |

All angles must use the same unit. Most programs use radians. The formulas below use a unit sphere. If the sphere has radius \(R\), multiply the final map coordinates by \(R\), or use matching map units everywhere.

## Forward Projection

Let the projection center have latitude \(\phi_1\) and longitude \(\lambda_0\). Let the point on the sphere have latitude \(\phi\) and longitude \(\lambda\).

First compute the longitude difference:

\[
\Delta\lambda = \lambda - \lambda_0
\]

The angular distance \(c\) from the center is defined by:

\[
\begin{aligned}
\cos c
&= \sin \phi_1 \sin \phi \\
&\quad + \cos \phi_1 \cos \phi \cos(\Delta\lambda)
\end{aligned}
\]

Then compute:

\[
k' = \frac{c}{\sin c}
\]

The projected flat coordinates are:

\[
x = k' \cos \phi \sin(\Delta\lambda)
\]

\[
\begin{aligned}
y
&= k'
\left[
\cos \phi_1 \sin \phi \right. \\
&\quad \left. - \sin \phi_1 \cos \phi \cos(\Delta\lambda)
\right]
\end{aligned}
\]

At the projection center, \(c=0\). The expression \(c/\sin c\) becomes \(0/0\), so use its limit:

\[
\lim_{c\to 0}\frac{c}{\sin c}=1
\]

That means \(k'=1\) at the center.

## What The Forward Formula Means

The value \(\Delta\lambda\) tells how far the point is east or west from the center. The value \(c\) tells how far the point is from the center on the sphere, measured as an angle.

The factor \(k'\) places the point on the flat map so that the radial distance from the center is correct. This is the key property of the projection. Distances from the center are preserved, but distances between two non-center points may be distorted.

## Key Idea

The central idea is that every point is placed by its direction and distance from one chosen center. The map keeps distances from the center correct. It does not keep all shapes, areas, or pairwise distances correct.

This makes the projection useful for center-based maps. For example, if a map is centered on one city, the distance from that city to every other place can be read correctly in scale.

## Reference

These formulas follow Eric W. Weisstein, [Azimuthal Equidistant Projection](https://mathworld.wolfram.com/AzimuthalEquidistantProjection.html), Wolfram MathWorld.
