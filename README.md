# GRoT> Graficzny Rozwiązywacz Tarcz
Linear FEM solver with nonlinear plasticity and postprocessor for strength analysis of 4-noded quadrilateral plane stress and strain elements obtained directly from bitmap file.

To run you need to install dependencies with: 
```
python3 -m pip install -r requirements.txt
```
Then just let the magic happen:
```
python3 run.py
```

What's new in 1.4.0:
- Plastcity! Bilinear isotropic hardening material model
- Second order Runge-Kutta algorithm for nonlinear calculations
- Probe function to check results in specified elements
- Principal strains and stresses, principal angles and invariants of tensors
- Huber stress after unloading
- Nice gallery html file with all of the results
- Bug fixes, element tweaking, efficiency improved


Check the example of gallery file:</br>
https://tutajrobert.github.io/grot/gallery.html</br>


Check old examples:</br>
https://tutajrobert.github.io/grot/galeria.html</br>
https://tutajrobert.github.io/grot-site/examples.html</br>


And you can check old websites for first release of GRoT></br>
[PL]: https://tutajrobert.github.io/grot/</br>
[ENG]: https://tutajrobert.github.io/grot-site/main.html</br>


But first of all write an email to me if you have any questions or just wanna talk about finite elements. I spent three years working with this software and gain some knowledge about finite elements.

Cheers!

Robert
