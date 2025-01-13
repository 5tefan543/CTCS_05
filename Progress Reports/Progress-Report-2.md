### What we did after the last meeting
1. Integrated our 'HelloWorld' program from before into the automatic benchmarking framework.
2. Fixed 'ZXing' program, and readded it to the benchmarking framework.
3. Added 'Mandelbrot' as new program with approximations to the benchmarking framework.
4. Tested Enerj for a 2D-HeatStencil application but found it to be unsuitable for the task.
5. Collected research data on more recent approximation strategies focusing on energy savings and different energy models. 
6. Started preparing the presentation slides.

### Findings

#### Integrating own annotaed programs into benchmarking framwork (Referencing points 3-4)
During the annotation and integration of custom programs into the benchmarking framework, we encountered several challenges and found some interesting results:

- The process of annotating custom programs was straightforward, as the EnerJ annotations are simple and easy to understand.
- During the integration of the 'Mandelbrot' program, we discovered significant limitations of the EnerJ framework. Specifically, it proved unsuitable for medium and large programs and configurations. The Mandelbrot.java program could only execute with small image configurations, such as a maximum resolution of 160x80 pixels. Even at this size, the EnerJ runtime consumed more than 9 GB of memory and required several minutes to complete a single execution, highlighting its inefficiency for testing on larger-scale applications. The Benchmarks from the paper are also configured to very low problem sizes.
- Additionally, we needed to modify the benchmarking logic of EnerJ for the Mandelbrot application, specifically the error calculation. The default EnerJ benchmarking logic, for example, compares string outputs from precise and approximate executions and returns an error of 100% if even a single character differs. This simplistic approach is unsuitable for applications like Mandelbrot, where outputs are arrays of image data rather than simple strings.
To address this, we updated the benchmarking process to include an 'error_script' option, which enables custom error calculations. For the Mandelbrot application, we collect the precise and approximate outputs (the image array data printed to the console) as usual. Instead of comparing the outputs directly as strings, the benchmarking script (collect.py) now invokes a custom Python script (calc_error.py) located in the Mandelbrot/ folder. This script receives the precise and approximate outputs, calculates the relative error pixel by pixel, aggregates the results, and returns the error rate as a percentage. The benchmarking script then collects and processes this error rate as usual.
This enhancement allows for more sophisticated and application-specific error calculations, not just for the Mandelbrot application but for any future program requiring customized error metrics. It represents a general and flexible solution for benchmarking diverse applications within the framework.
- In the case of the 2D-HeatStencil application, we determined that using approximations was not viable. The nature of this application — simulating heat distribution in a 2D grid — makes it highly sensitive to computational errors. Any inaccuracies in the calculations propagate across the grid, leading to entirely unreliable results. Therefore, we decided to not include the 2D-HeatStencil application in our benchmarking framework. We consider this am important finding. Even code segments which seem safe to approximate, and can tolerate small errors, may produce worthless results if errors are allowed to compound or propagate. Our survey Paper mentions this as one of the main challenges in approximate computing.

#### Research on Approximation Strategies (Referencing point 5)
Our investigations into recent approximation strategies and energy models are ongoing. Below is a summary of our progress in this area:

- **Memory Approximation**: 
  - We found several recent publications, some of which are approximately related to methods simulated in EnerJ, as well as 2-3 new approaches.
  - Some data on energy savings has been extracted. However, integrating these findings into our simulation is challenging because many studies focus on highly specific applications (e.g., specialized hardware, embedded systems, ML accelerators). 
  - Additionally, errors are often reported in domain-specific contexts (e.g., accuracy loss in ML tasks), making them difficult to simulate within EnerJ.

- **Computation Approximation**:
  - This area is less well-covered in our research so far. There are numerous proposals for approximate variations of components, from the transistor level to the architectural level. 
  - Determining which of these could be relevant to our purposes and linking them to energy savings (e.g., through saved CPU cycles) is not straightforward.
  - Unlike memory approximation strategies, we have yet to find hardware examples (e.g., CPUs with approximate and precise cores with differing energy costs for basic operations).

### Next Steps

- Finishing the presentation slides.
- Start writing the final report.
- Continue researching approximation strategies and energy savings as well as energy models?
- Implementing more benchmarks?
