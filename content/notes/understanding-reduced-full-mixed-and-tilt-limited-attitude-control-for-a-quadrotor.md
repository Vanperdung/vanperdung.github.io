+++
title       = 'Understanding Reduced, Full, Mixed, and Tilt-Limited Attitude Control for a Quadrotor'
date        = '2026-07-07T00:00:00+07:00'
draft       = false
description = 'Notes on reduced, full, mixed, and tilt-limited attitude control for a quadrotor.'
tags        = ['Quadrotor', 'Attitude Control', 'Control Systems', 'Robotics']
math        = true
+++

# Understanding Reduced, Full, Mixed, and Tilt-Limited Attitude Control for a Quadrotor

## Purpose of this note

This note explains the attitude-command ideas in **“Nonlinear Quadrocopter Attitude Control”** by Brescianini, Hehn, and D’Andrea. The main goal is to show how a quadrotor turns a desired motion into a desired attitude. It explains reduced attitude control, full attitude control, the mixing method used in the paper, and maximum tilt limiting. The language is kept simple, but the main equations are included so that the ideas can be used in an implementation.

This note uses unit quaternions that rotate body-frame vectors into the world frame. With this active convention, an attitude correction multiplies on the left. Different software libraries may use a different convention for quaternion order or frame direction. Therefore, do not copy a quaternion product blindly. After building a desired attitude, always check that the body thrust axis points in the desired direction when it is expressed in the world frame.

---

## 1. The main control idea

A quadrotor has an outer position controller and an inner attitude controller. The position controller looks at the desired path, the current position, and the current velocity. It then decides which acceleration the vehicle should create. The attitude controller receives this acceleration request and turns it into a desired orientation. A faster onboard controller then changes the motor thrusts so that the real vehicle follows this orientation.

The key point is that a quadrotor cannot push directly to the left, right, forward, or backward. Its rotors mainly create one total thrust force along the vehicle body \(z\)-axis. To move sideways, the quadrotor must tilt this thrust force. Once the thrust vector has a horizontal part, that horizontal part accelerates the quadrotor in the desired direction.

Let \(I\) be the inertial or world frame, and let \(B\) be the body frame fixed to the quadrotor. The body thrust axis is \(\mathbf{e}_z^{B}\). When it is written in the world frame, it is

\[\mathbf{b}_3 = {}^{I}\mathbf{e}_z^{B}.\]

The exact sign of thrust depends on the frame convention. In some systems, thrust points along \(+\mathbf{b}_3\); in others, it points along \(-\mathbf{b}_3\). This note follows the geometric idea in the paper: the desired thrust axis should point along the normalized desired acceleration or force direction.

If the outer controller gives a vector \({}^{I}\mathbf{a}_{\mathrm{cmd}}\), the paper writes the desired thrust direction and collective thrust as

\[{}^{I}\mathbf{e}_{\mathrm{cmd},z}^{B} = \frac{{}^{I}\mathbf{a}_{\mathrm{cmd}}} {\left\|{}^{I}\mathbf{a}_{\mathrm{cmd}}\right\|}, \qquad \mathrm{coll}_{\mathrm{cmd}} = \left\|{}^{I}\mathbf{a}_{\mathrm{cmd}}\right\|.\]

In a real flight controller, the vector used here must follow the chosen gravity and thrust-sign convention. For example, the desired force may include gravity compensation before it is normalized. The important idea is simple: the outer loop gives the direction in which the total thrust should point, and the attitude loop makes the body \(z\)-axis point in that direction.

---

## 2. Why thrust direction is not the full attitude

A full attitude has three degrees of freedom. However, a unit thrust direction has only two degrees of freedom. It tells the quadrotor how to tilt, but it does not tell the quadrotor how to rotate around its own thrust axis.

Imagine that the quadrotor already tilts correctly to fly north. It can still turn its nose while keeping the same tilt and the same thrust direction. In an ideal model, this nose direction does not change the translational force. This remaining freedom is usually called heading or yaw.

For this reason, the position controller does not have to provide yaw. It provides the thrust direction needed for motion. A yaw command, written as \(\psi_{\mathrm{cmd}}\), usually comes from another source. It may come from the pilot, the path planner, a camera task, a target-tracking task, or a rule such as “make the nose point along the velocity direction.”

This leads to three useful control choices. Reduced attitude control uses only the desired thrust direction. Full attitude control uses both the desired thrust direction and the desired yaw. Mixed attitude control keeps the thrust direction correct while giving yaw a lower priority.

---

## 3. The quaternion attitude controller in the paper

After a desired quaternion \(q_{\mathrm{cmd}}\) has been built, calculate the left-multiplicative attitude error as

\[q_e = q_{\mathrm{cmd}}\otimes q^{-1}.\]

where \(q\) is the current attitude. Equivalently,

\[q_{\mathrm{cmd}} = q_e\otimes q.\]

This error quaternion describes the rotation needed to move from the current attitude to the commanded attitude. Its rotation axis is expressed in the world frame. If the rate controller expects a body-frame angular-rate command, convert the command consistently before using it.

The paper uses the following angular-rate command:

\[\boldsymbol{\Omega}_{\mathrm{cmd}} = \frac{2}{\tau} \operatorname{sgn}(q_{e,0})\,\mathbf{q}_{e,1:3}.\]

Here, \(q_{e,0}\) is the scalar part of the quaternion, \(\mathbf{q}_{e,1:3}\) is its vector part, and \(\tau\) is a time constant. The sign choice matters because \(q\) and \(-q\) describe the same physical attitude. It makes the controller choose the quaternion form that represents a rotation of at most \(180^\circ\). In simple words, the controller tries to turn through the shorter angular path instead of making an unnecessary full turn.

The commanded angular rate is bounded by

\[\left\|\boldsymbol{\Omega}_{\mathrm{cmd}}\right\| \leq \frac{2}{\tau}.\]

This bound is useful because motors and rate controllers have limits. Still, the sign change creates a discontinuity near a \(180^\circ\) attitude error. With noisy attitude data, a practical system should avoid rapid sign changes near that point. A sampled controller already helps because its output stays fixed between control updates, but a small hysteresis or careful thresholding can also be useful.

---

## 4. Reduced attitude control

Reduced attitude control asks one question: **what is the shortest rotation that moves the current thrust direction to the desired thrust direction?** It does not ask the quadrotor to face a special heading at the same time.

Let the current thrust direction be

\[\mathbf{b}_3 = {}^{I}\mathbf{e}_z^{B},\]

and let the desired thrust direction be

\[\mathbf{b}_{3,d} = {}^{I}\mathbf{e}_{\mathrm{cmd},z}^{B}.\]

The angle between these two directions is

\[\alpha = \arccos\left(\mathbf{b}_3^\top\mathbf{b}_{3,d}\right).\]

When the two directions are not parallel, the shortest rotation axis is

\[\mathbf{k} = \frac{\mathbf{b}_3\times\mathbf{b}_{3,d}} {\left\|\mathbf{b}_3\times\mathbf{b}_{3,d}\right\|}.\]

The reduced error quaternion is

\[q_{e,\mathrm{red}} = \begin{bmatrix} \cos(\alpha/2)\\ \mathbf{k}\sin(\alpha/2) \end{bmatrix}.\]

The reduced error is a world-frame rotation, so the reduced desired attitude is

\[q_{\mathrm{cmd,red}} = q_{e,\mathrm{red}}\otimes q.\]

This target makes the thrust axis point exactly along \(\mathbf{b}_{3,d}\). It does not directly set a yaw target. That is why reduced attitude is good when the main task is to accelerate, brake, or follow a path quickly.

It is common to say that reduced attitude controls roll and pitch but ignores yaw. This is a useful idea near hover, but it is not fully correct for large angles. The more exact statement is that reduced attitude controls the two degrees of freedom of the thrust direction and leaves free the rotation around that direction. Because Euler angles are linked to each other, the Euler yaw value can still change during a reduced-attitude move.

### Important special cases

The cross product in the rotation-axis equation can become very small. Code must handle this safely. If

\[\mathbf{b}_3^\top\mathbf{b}_{3,d}\approx 1,\]

then the thrust axes are already aligned, so the reduced error quaternion should be the identity quaternion. If

\[\mathbf{b}_3^\top\mathbf{b}_{3,d}\approx -1,\]

then the desired axis is exactly opposite to the current axis. The needed angle is \(\pi\), but there is no unique rotation axis. The code must choose any stable unit axis perpendicular to \(\mathbf{b}_3\). For example, it can cross \(\mathbf{b}_3\) with a reference axis that is not almost parallel to \(\mathbf{b}_3\).

---

## 5. Full attitude control

Full attitude control adds a desired yaw angle \(\psi_{\mathrm{cmd}}\) to the desired thrust direction \(\mathbf{b}_{3,d}\). These two values define one desired attitude, apart from the usual Euler-angle singular cases.

The paper uses ZYX Euler angles. In this order, yaw is first applied around the original world \(z\)-axis. Pitch and roll are then chosen so that the body thrust axis still points in the desired direction. This is important because a world-yaw rotation is not the same as a rotation around the already tilted thrust axis, except when the vehicle is close to hover.

The paper builds the full attitude directly instead of starting with reduced attitude and guessing a yaw twist. First, it creates an intermediate frame \(K\) by rotating the world frame by the desired yaw \(\psi_{\mathrm{cmd}}\). You can think of frame \(K\) as a frame that has the correct heading but has not tilted yet.

The desired thrust direction is written in this yaw-aligned frame as

\[{}^{K}\mathbf{e}_{\mathrm{cmd},z}^{B} = R_{KI}(\psi_{\mathrm{cmd}}) {}^{I}\mathbf{e}_{\mathrm{cmd},z}^{B},\]

where

\[R_{KI}(\psi_{\mathrm{cmd}}) = \begin{bmatrix} \cos\psi_{\mathrm{cmd}} & \sin\psi_{\mathrm{cmd}} & 0\\ -\sin\psi_{\mathrm{cmd}} & \cos\psi_{\mathrm{cmd}} & 0\\ 0 & 0 & 1 \end{bmatrix}.\]

The pitch command is then chosen from the projection of the desired thrust direction in the \(x_K-z_K\) plane:

\[\theta_{\mathrm{cmd}} = \operatorname{atan2} \left( {}^{K}e_{\mathrm{cmd},z,1}^{B}, {}^{K}e_{\mathrm{cmd},z,3}^{B} \right).\]

The paper writes this step as an arctangent of a ratio. In software, \(\operatorname{atan2}\) is safer because it gives the correct angle quadrant and does not divide by zero.

Next, the paper creates frame \(L\) by applying the pitch rotation:

\[{}^{L}\mathbf{e}_{\mathrm{cmd},z}^{B} = R_{LK}(\theta_{\mathrm{cmd}}) {}^{K}\mathbf{e}_{\mathrm{cmd},z}^{B},\]

with

\[R_{LK}(\theta_{\mathrm{cmd}}) = \begin{bmatrix} \cos\theta_{\mathrm{cmd}} & 0 & -\sin\theta_{\mathrm{cmd}}\\ 0 & 1 & 0\\ \sin\theta_{\mathrm{cmd}} & 0 & \cos\theta_{\mathrm{cmd}} \end{bmatrix}.\]

The roll command is the remaining rotation needed to match the thrust direction:

\[\phi_{\mathrm{cmd}} = \operatorname{atan2} \left( -{}^{L}e_{\mathrm{cmd},z,2}^{B}, {}^{L}e_{\mathrm{cmd},z,3}^{B} \right).\]

Finally, the full target quaternion is made from the three Euler angles:

\[q_{\mathrm{cmd,full}} = q(\psi_{\mathrm{cmd}},\theta_{\mathrm{cmd}},\phi_{\mathrm{cmd}}).\]

The logic is therefore clear: first choose the desired heading, then find the pitch and roll that keep the thrust axis in the correct direction.

### Why not simply add the yaw error to reduced attitude?

A natural idea is to build the reduced target first and then add a twist with angle \(\psi_{\mathrm{cmd}}-\psi\). This is not correct in general. The Euler yaw difference is a world-referenced rotation in the ZYX definition. A twist added to an already tilted attitude is a rotation around the thrust axis. When the quadrotor is tilted, these two axes are not the same.

However, your geometric observation is still useful. If the quadrotor first rotates around its current body \(z\)-axis, its current thrust direction does not change. Therefore, the reduced-attitude angle \(\alpha\) and the inertial rotation axis \(\mathbf{k}\) also do not change. The hard part is not preserving the reduced construction. The hard part is finding the exact twist angle that will give the chosen final Euler yaw. The paper avoids this problem by building \(q_{\mathrm{cmd,full}}\) directly from \(\mathbf{b}_{3,d}\) and \(\psi_{\mathrm{cmd}}\).

---

## 6. The meaning of \(q_{\mathrm{mix}}\)

Reduced attitude and full attitude have the same desired thrust direction. Therefore, they differ only by a rotation around that common thrust direction. With the left-multiplicative convention, this difference is

\[q_{\mathrm{mix}} = q_{\mathrm{cmd,full}} \otimes q_{\mathrm{cmd,red}}^{-1}.\]

This equation answers a simple question: **after reaching the reduced target, what rotation is still needed to reach the full target?** The same relation can be written as

\[q_{\mathrm{cmd,full}} = q_{\mathrm{mix}} \otimes q_{\mathrm{cmd,red}}.\]

The axis of \(q_{\mathrm{mix}}\) is the common thrust direction in the world frame. Therefore, it has the form

\[q_{\mathrm{mix}} = \begin{bmatrix} \cos(\alpha_{\mathrm{mix}}/2)\\ \mathbf{b}_{3,d}\sin(\alpha_{\mathrm{mix}}/2) \end{bmatrix}.\]

The angle \(\alpha_{\mathrm{mix}}\) is the twist angle between the reduced and full targets. It is not simply the Euler yaw error. It is the actual rotation around the target thrust axis that turns the reduced target into the full target.

---

## 7. Mixed reduced and full attitude control

Pure reduced attitude gives all priority to thrust direction. Pure full attitude tries to correct the thrust direction and yaw at the same time. The paper introduces mixing because yaw motion is usually slower than roll and pitch motion. In addition, the commanded angular-rate vector has a limited size. If the controller spends too much of that limited command on yaw, the quadrotor may tilt more slowly even when fast tilt is needed for the path.

The mixed target uses only part of the world-frame twist from reduced attitude to full attitude:

\[q_{\mathrm{cmd}} = \begin{bmatrix} \cos(p\alpha_{\mathrm{mix}}/2)\\ \mathbf{b}_{3,d}\sin(p\alpha_{\mathrm{mix}}/2) \end{bmatrix}\otimes q_{\mathrm{cmd,red}}, \qquad p\in[0,1].\]

When \(p=0\), no twist is added, so the result is pure reduced attitude:

\[q_{\mathrm{cmd}}=q_{\mathrm{cmd,red}}.\]

When \(p=1\), the full twist is added, so the result is pure full attitude:

\[q_{\mathrm{cmd}}=q_{\mathrm{cmd,full}}.\]

For a value such as \(p=0.3\), the target attitude has the exact correct thrust direction, but it includes only \(30\%\) of the twist toward the full yaw target at that instant. Since the target is calculated again at every control step, yaw still moves toward the desired value over time. It simply moves more slowly, so the controller can give more immediate priority to tilt.

The paper gives a bound for the yaw-rate part of the command:

\[\left|\Omega_{\mathrm{cmd},z}\right| \leq \frac{2\sin(p\pi/2)}{\tau}.\]

For small yaw errors, the paper relates \(p\) to two time constants:

\[p = \frac{\tau}{\tau_{\mathrm{yaw}}}.\]

Here, \(\tau\) is the desired response time for pitch and roll, while \(\tau_{\mathrm{yaw}}\) is a slower desired response time for yaw. The paper gives \(\tau=0.08\,\mathrm{s}\) and \(\tau_{\mathrm{yaw}}=0.2\,\mathrm{s}\) as one experiment, which gives \(p=0.4\). These values are not universal. A different quadrotor needs its own tuning based on motor power, inertia, thrust level, rate limits, and the onboard rate controller.

Mixing does not say that yaw is unimportant in every task. A camera drone, inspection drone, or docking drone may need strong yaw control. In such a task, \(p\) may need to be larger, or it may need to change with the mission state.

---

## 8. Limiting the maximum tilt angle

A controller may need to prevent the commanded attitude from tilting too far. This can protect a payload, keep enough vertical thrust for altitude control, preserve camera view, keep motor margin, and make the motion easier to predict.

The paper defines the commanded tilt angle as the angle between the world vertical axis and the desired thrust direction:

\[\alpha_{\mathrm{tilt}} = \arccos\left( ({}^{I}\mathbf{e}_z)^\top {}^{I}\mathbf{e}_{\mathrm{cmd},z}^{B} \right).\]

If

\[\alpha_{\mathrm{tilt}}\leq\alpha_{\max},\]

then the desired direction is already allowed. If it is larger than \(\alpha_{\max}\), the desired direction should be moved back to the edge of an allowed cone around the world vertical axis. The new direction should still point toward the same horizontal side, but it should have exactly the allowed tilt angle.

A clear way to compute this is to first take the horizontal part of the desired direction:

\[\mathbf{h} = \mathbf{b}_{3,d} - \left((\mathbf{e}_z^{I})^\top\mathbf{b}_{3,d}\right)\mathbf{e}_z^{I}.\]

If \(\|\mathbf{h}\|\) is not close to zero, normalize it:

\[\hat{\mathbf{h}} = \frac{\mathbf{h}}{\|\mathbf{h}\|}.\]

The limited thrust direction is then

\[\mathbf{b}_{3,d}^{\mathrm{lim}} = \cos(\alpha_{\max})\mathbf{e}_z^{I} + \sin(\alpha_{\max})\hat{\mathbf{h}}.\]

This means: keep the requested horizontal direction, but reduce the tilt to the largest allowed value. After this step, every later calculation—reduced attitude, full attitude, and mixing—must use \(\mathbf{b}_{3,d}^{\mathrm{lim}}\), not the old unlimited direction.

The paper also presents this idea as a rotation around the axis between the vertical direction and the desired thrust direction. In implementation, make sure the rotation axis is built with a normalized cross product. This avoids numerical problems and makes the geometric meaning clear.

---

## 9. What changes when tilt is limited

A tilt limit makes some acceleration commands impossible. For example, the outer controller may request a direction that needs \(60^\circ\) of tilt, but the system may allow only \(30^\circ\). The quadrotor will still tilt toward the correct side, but it cannot create the requested horizontal force. It may turn more slowly, brake more slowly, fall behind the path, or fail to hold its position against strong wind.

If the quadrotor must keep altitude and has enough total thrust, a useful rough limit is

\[a_{xy,\max}\approx g\tan(\alpha_{\max}).\]

This shows that a smaller tilt limit means a smaller maximum horizontal acceleration. More generally, if the total thrust is \(T\), the vehicle mass is \(m\), and the tilt is \(\alpha\), then the horizontal thrust acceleration is approximately

\[a_{xy}= \frac{T}{m}\sin\alpha.\]

The vertical part is approximately

\[a_z= \frac{T}{m}\cos\alpha-g,\]

with signs adjusted for the chosen world-frame convention. These equations show that horizontal acceleration, vertical acceleration, total thrust, and tilt are linked.

Tilt limiting can also affect altitude. The outer controller may have chosen a collective thrust value for an unlimited force direction. After the direction is limited, the vertical part of the real thrust may no longer match the requested vertical force. If collective thrust is not handled consistently, the quadrotor may climb or lose altitude while the tilt limit is active.

Another issue is integrator windup. If the position controller has an integral term, position error can keep growing while the tilt limit prevents the vehicle from producing enough horizontal acceleration. When the command becomes possible again, the stored integral value can cause overshoot. Anti-windup logic, command limiting in the outer loop, or conditional integration can reduce this problem.

A hard tilt clamp can also make commands less smooth near \(\alpha_{\max}\). A small change in desired acceleration can switch the command between “not limited” and “limited.” If this happens often because of noise or fast outer-loop changes, the desired attitude and motor commands may shake. A smooth saturation can reduce the tilt gain gradually near the limit. A reference filter can limit how quickly the desired thrust direction is allowed to move. These methods do not remove the physical limit; they only make the change near the limit smoother and easier for the inner loop to follow.

Finally, a tilt limit does not guarantee that the real vehicle can never flip. It limits the target attitude, not the current attitude. A strong disturbance, high angular speed, or an already bad orientation can still cause a large recovery rotation.

---

## 10. A practical command-building order

A complete control update can follow this connected sequence. The outer controller first produces a desired force or acceleration. Convert this request, with the correct gravity and thrust sign, into a desired thrust direction and a collective thrust value. Then apply the maximum tilt limit to the thrust direction when needed.

Next, use the limited thrust direction to build the reduced attitude target. Obtain a yaw command from the mission, pilot, path planner, or heading rule. If there is no yaw task, use reduced attitude only. If yaw is needed, build the full attitude directly from the limited thrust direction and the desired yaw using the paper’s yaw–pitch–roll construction.

Once both targets exist, calculate

\[q_{\mathrm{mix}} = q_{\mathrm{cmd,full}} \otimes q_{\mathrm{cmd,red}}^{-1}.\]

Choose \(p\) based on how much yaw priority the task needs. Use the mixing formula to build the final target quaternion. Finally, calculate the quaternion attitude error and use the attitude control law to produce the commanded angular rate.

During simulation and hardware tests, always check this condition:

\[R(q_{\mathrm{cmd}})\mathbf{e}_z^{B} \approx \mathbf{b}_{3,d}^{\mathrm{lim}}.\]

This test confirms that the final target attitude still points the thrust axis in the desired limited direction. It is one of the best ways to find mistakes in frame definitions, quaternion order, or multiplication order.

---

## 11. Main ideas to remember

The position controller mainly decides where the thrust vector must point. This decides the motion of the quadrotor. The thrust direction alone does not decide the nose direction, so a separate yaw command is needed for full attitude control.

Reduced attitude control makes the thrust axis point correctly and does not directly control heading. Full attitude control sets both thrust direction and yaw. The paper builds full attitude by first choosing yaw around the world vertical axis, then choosing pitch and roll so that the thrust direction stays correct.

The quaternion

\[q_{\mathrm{mix}} = q_{\mathrm{cmd,full}} \otimes q_{\mathrm{cmd,red}}^{-1}\]

is the rotation still needed to move from the reduced target to the full target. Mixing takes only part of this rotation, so the quadrotor can tilt quickly for translation while yaw moves toward its target more slowly.

Maximum tilt limiting should happen before reduced attitude, full attitude, or mixing is built. It keeps the desired thrust direction inside an allowed cone. This improves safety and control margin, but it also limits horizontal acceleration and can create path error, altitude coupling, integrator windup, and command shaking if it is not handled carefully.

---

## Reference

Dario Brescianini, Markus Hehn, and Raffaello D’Andrea, *Nonlinear Quadrocopter Attitude Control*, Technical Report, ETH Zürich, 2013. The main sections used here are Sections 2.2, 3.1, 3.2, 3.3, and 4.2.
