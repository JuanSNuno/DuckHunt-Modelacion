# Project Overview

DuckHunt-JS is an implementation of the classic DuckHunt game using JavaScript and HTML5. It utilizes the PixiJS rendering engine (supporting WebGL and Canvas), GreenSock (GSAP) for tweening animations, and HowlerJS for audio (WebAudioAPI with fallback to HTML5 Audio). The main game logic is implemented in ES6 classes that are transpiled to ES5 using Babel.

## Building and Running

The project requires Node.js. Install dependencies with `npm install` before running any commands.

### Local Development Server
To start a local development webserver (hosted on `http://localhost:8080/`):
```bash
npm start
```
This runs `webpack-dev-server` and will trigger automatic rebuilds and page reloads when changes are detected in the `src` directory.

### Build Production Code
To manually build the application code into the `dist` directory:
```bash
npm run build
```

### Building Assets (Audio and Images)
Rebuilding the audio and image assets requires additional system dependencies.
- **Audio:** `npm run audio` (Requires `ffmpeg` to run the gulp task)
- **Images:** `npm run images` (Requires `TexturePacker` to run the gulp task)

## Development Conventions

- **Code Structure:** The main game logic is broken down into ES6 classes located in the `src/modules` directory (e.g., `Game.js`, `Duck.js`, `Dog.js`, etc.).
- **Linting:** Code style and quality are enforced using ESLint. Run the linter using:
  ```bash
  npm run lint
  ```
- **Transpiling:** Babel is used to transpile modern JavaScript via `babel-loader` in Webpack.
- **Asset Processing:** Gulp is used alongside external tools to process sounds into audio sprites and images into sprite sheets.
