# GRoT> Graficzny Rozwiązywacz Tarcz
GRoT> is the linear Finite Element Method solver, pre and postprocessor with nonlinear plasticity. Use for strength analysis of simple geometries built of 4-noded quadrilateral plane stress and strain elements. Its most unique function is the easy input of geometry of models, which is taken directly from an image saved as a bitmap file.

![Plastic strains](https://tutajrobert.github.io/grot/pl_strain.png "Plastic strains plot")

## Example
Check the example of gallery file:</br>
https://tutajrobert.github.io/grot/gallery.html</br>

## Core
- Input is taken as a bitmap file prepared in any graphic editor
- Constant strain, square finite element with four nodes and linear shape functions according to *Rakowski, Kacprzyk: Metoda Elementów Skończonych w mechanice konstrukcji*
- Results are saved as matplotlib plots with a coolwarm aesthetic colour map for viewing pleasure
- Variety of results for strains and stresses: Huber equivalent, signed equivalent, tensor components, principals, invariant, principal angles
- Plasticity! Bilinear isotropic hardening material model
- Second-order Runge-Kutta algorithm for nonlinear calculations

## Installation
To run, you need to install dependencies with: 
```
python3 -m pip install -r requirements.txt
```
Then just let the magic happen:
```
python3 run.py
```

## Brief description of how to analyse

Performing an analysis in GRoT> requires the use of various support programs. To prepare the geometry, use simple graphical software like Paint, Tux Paint, and mtPaint. Analysis settings and boundary conditions are set in a text file *input.txt* that one can edit in any text editor, such as Notepad, Word or Notepad ++. Running the computational procedure is executed as a single Python command. The plots of results (in png format) are stored in the project directory.

Five steps to run an analysis:
1. Go to the just downloaded GRoT> directory.
2. Create geometry as a bitmap image and save it in the projects folder.
3. Modify input file input.txt to set up analysis options.
4. In console or terminal, run Python script run.py to perform analysis.
5. View graphical results stored in the results folder.

## Graphical input

The created bitmap file of any name should be stored in the *projects* directory in the GRoT> folder. The input bitmap file will be translated to the finite element model, where one image pixel corresponds to a single, square finite element. Using the appropriate colours allows the software to read the bitmap image as a computational model with the corresponding boundary conditions assigned.

### Boundary conditions / colors description

- Body of model (just finite elements): cyan or light blue
- Lack of elements, empty: white
- Constraints: in the horizontal direction, vertical and both: red, green, dark blue
- Force load in nodes of FE (max 3): magenta, brown, black
- Probed elements for which exact results are stored: magenta, brown, black

## Have a great day!
But most of all, write an email to me if you have any questions or want to talk about finite elements. I spent three years working with this software and gained quite a knowledge about finite elements.

## Mail me
I work as an FEA and CFD engineer. I spend most of my time dealing with the analysis of steel structures and flows in hydraulic equipment. In my free time, I try to force the Python programming language to cooperate with me in the field of numerical analysis. I will be happy if you contact me: tutajrobert@vp.pl.

Cheers!

Robert
