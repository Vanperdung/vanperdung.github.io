+++
title       = 'Understanding FFTs and Windowing'
date        = '2026-04-03T00:00:00+07:00'
draft       = false
description = ''
tags        = ['FFTs', 'Quadcopter']
+++

## Overview

The Fourier Transform is a powerful tool for identifying errors and noise in signals.

Although the Fourier Transform involves complex mathematics, you do not need to be a math expert to understand the concept.

The Fourier Transform essentially breaks a signal down into sine waves of different amplitudes and frequencies. Let's take a deeper look at what this means and why it is useful.

## All signals are sum of sines

Any signal in the time domain (a plot of signal value over time) can be represented as a sum of sine waves. To find out exactly which sine waves make up a signal, we use the FFT (Fast Fourier Transform) to convert the signal from the time domain to the frequency domain.

The resulting frequency-domain diagram shows the amplitude of each sine wave at different frequencies. From this diagram, we can easily identify which sine waves - and at what amplitudes - are present in the original signal.

## Sample window

To produce the frequency-domain diagram, the FFT requires a sample window - a finite set of samples taken from the signal you want to analyze.

The window size is typically a power of 2 (e.g. 256, 512, 1024). The larger the window size, the higher the computation time and memory usage.

The FFT assumes the window fits a whole number of signal periods. In practice, this is rarely true - the signal is cut off mid-period at the window edge. This causes **spectral leakage**: energy from one frequency spills into neighboring frequency bins, making each peak in the spectrum appear wider and lower than it really is.

## Hanning window

The Hanning window is a way to reduce spectral leakage.

It works by scaling the samples so that they fade smoothly to zero at both ends of the window. This removes the sharp jump at the edges, which is the main cause of spectral leakage.

The trade-off is that it slightly reduces the ability to tell apart two close frequencies.

The result below describes the improvement of applying hann window:

![Spectral leakage comparison](/images/spectral_leakage.png)

# References

[FFTs-and-windowing](https://download.ni.com/evaluation/pxi/Understanding%20FFTs%20and%20Windowing.pdf)



