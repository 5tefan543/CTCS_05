### What we did after the last meeting

1. Contacted the original author of the paper and actually got sent the missing parts of the source code.
2. Set Up a Docker container, making the old project buildable and executable with its old dependencies.
3. Spent time understanding different parts of the Software Code and its Execution as much as possible. 
4. Created a Hello World+ program with `@Approx` annotations, compiled and executed it with the software. 
5. Benchmarked the same programs (excluding one) as in the paper, with the same approximation simulation strategies.
6. Created a python script, that generates plots similar to the ones used in the paper from the benchmark data. 
7. Integrated our Hello World program from before into the automatic Benchmarking-Framework.
##### 8. Conducted Research on the Developments of Approximating Hardware. 
Findings:
1. Research on approximation strategies has continued and is very active, Still very concept/experimental. Little empirical-testing on actual hardware. 2011-2015 was a very active phase, with the original author (A. Sampson) being mentioned often. In the last years the topic has been resurging. We found an extensive 02.09.24 research article (survey), containing or pointing towards many developments on approximate computing (More than EnerJ targets). 

2. FlexJava (2015) is a project building directly on EnerJ, rethinking the annotation concept from EnerJ, and simplifying the creation of approximate programs for developers. It also slightly expands on EnerJ in terms of approximation strategies implemented. It reaches the same simulated energy savings, as EnerJ, using the same approximation strategies, but significantly less annotations (on the same programs).

### Next Steps ?

Ways we could see to move forward in our project:

- Transform more programs to approximate ones, using the EnerJ language extension. Document the effort of learning and performing this task, and include those programs in our Benchmarking.
	(effort depends on programs)

- Try building and and running FlexJava. Benchmark programs there? Compare using those frameworks / performance aspects.

- adjust energy-saving simulations and error rates to more closely resemble current technologies
	(implementation easy, but very research intensive, because concept papers focusing on performance, not energy, and few empirical studies)

- Add additional approximation simulations and integrate them into the runtime.
	(implementation more challenging, also a lot of research)

- Modify or extend anything within the compiler or language. 
	(very hard, we prefer to avoid this)
