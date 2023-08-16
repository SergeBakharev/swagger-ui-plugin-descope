import esbuild from 'esbuild'
import process from 'process'
import { NodeModulesPolyfillPlugin } from '@esbuild-plugins/node-modules-polyfill'
import yargs from 'yargs'
import { hideBin } from 'yargs/helpers'
import fs from 'fs'

const argv = yargs(hideBin(process.argv)).argv
const prod = argv._.indexOf('production') >= 0

/** @type {esbuild.BuildOptions} */
const distOptions = {
    banner: {
        js: '// Project: https://github.com/SergeBakharev/swagger-ui-plugin-descope',
    },
    entryPoints: [{
        in: './src/swagger-ui-plugin-descope.tsx',
        out: 'swagger-ui-plugin-descope',
    }],
    bundle: true,
    mainFields: ["browser", "module", "main"],
    format: 'esm',
    logLevel: 'info',
    sourcemap: false,
    treeShaking: true,
    outdir: './dist',
    minify: true,
    platform: 'browser',
    splitting: false,
    target: [
        'chrome58',
        'edge18',
        'firefox57',
        'safari11',
    ],
    plugins: [
        NodeModulesPolyfillPlugin(),
    ],
}

esbuild.build(distOptions).catch(() => process.exit(1))
