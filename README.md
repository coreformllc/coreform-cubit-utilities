# Coreform Cubit Utilities
Contains open source scripts, importers/exporters and other utilities for [Coreform Cubit](https://coreform.com)

## Contributing
We encourage contributions from the Coreform Cubit community!
If you would like to contribute your scripts, fork this repository and make your proposed changes.
Then open a pull-request to this main repository and we'll review and help you merge.

## Style Guide
* Python3 only: Python2 commands _will only_ be accepted if an accompanying Python3 command is provided.
* Python scripts should use two spaces for indenting as this is the convention with Cubit's internal parser (which is set at compile-time).
* Python scripts should include a documentation block
* Method names should follow [snake-case](https://en.wikipedia.org/wiki/Snake_case) naming to match Cubit's built-in Python naming conventions.
* Use [formatted string literals (aka f-strings)](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) for string interpolation, whenever possible e.g.
   *  **Correct:** `cubit.cmd(f"volume {vid} copy")` 
   *  Incorrect: `cubit.cmd("volume {vid} copy".format(vid)")`
   *  Incorrect: `cubit.cmd("volume " + vid[0] + " " + vid[1] + " copy")`
   *  Incorrect: `cubit.cmd("volume %d %d copy" %(vid[1],vid[2]))`
* Minimize use of Python libraries not in the distribution
   *  If your script is much simpler / performant / extensible / powerful through an external library (e.g. SciPy, NumPy) include this requirement in your script's documentation and add checks to see if module has been imported

## Future Work
* Include repository in Coreform's internal CI/CD for Cubit
  * Write tests for each script
  * Support 3rd-party repositories "hooking into" Coreform's internal CI/CD
    * e.g. [Paramak](https://github.com/fusion-energy/paramak), [MOOSE](https://github.com/idaholab/moose), [Firedrake](https://github.com/firedrakeproject/firedrake)
* Add UI utilities (e.g. user-defined toolbars, user-defined GUI commands)
* Add directory for mesh import/export utilities
