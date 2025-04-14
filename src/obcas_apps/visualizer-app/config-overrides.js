const path = require("path");

const { override, babelInclude } = require("customize-cra");

module.exports = function (config, env) {
  return Object.assign(
    config,
    override(
      babelInclude([
        /* transpile (converting to es5) code in src/ and shared component library */
        path.resolve("src"),
        /* toma estos cuando usamos la web en standalone */
        path.resolve("./node_modules/@condor/utils"),
        /* Toma estos cuando usamos la webapp en workspace */
        path.resolve("../../utils/trunk"),
      ])
    )(config, env)
  );
};