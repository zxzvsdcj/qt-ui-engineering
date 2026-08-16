# Anti-AI-Slop

## Failure pattern

Generated UI becomes generic when visual choices come from fashionable defaults instead of the product. Common symptoms are:

- every region wrapped in a rounded card;
- large headings and blank space used to imply quality;
- arbitrary purple/blue gradients, glow, glass, or shadow;
- repeated metric tiles without a real comparison task;
- emoji used as application icons;
- one SaaS dashboard layout applied to unrelated desktop tools;
- animation and decoration without state or causal meaning.

## Positive recipe

1. Name the product, users, main task, and highest-cost mistake.
2. Derive visual language from domain artifacts, instruments, signals, documents, and workflows.
3. Select one restrained signature that improves recognition or operation.
4. Build hierarchy from information, alignment, typography, and state.
5. Use native desktop structures when they improve throughput.
6. Remove any ornament that cannot explain its product or interaction function.

## Self-critique

Before implementation, ask whether the same palette, layout, typography, and decorative treatment would appear for an unrelated product. Revise generic parts. After implementation, review a rendered interface when possible and remove one unnecessary flourish before adding another.

Controlled density can be distinctive. Sparse or maximal visual directions are allowed only when the brief genuinely requires them; the default for operational Qt tools remains efficient, structured, and clear.

## Widget engineering anti-pattern index

Treat these engineering shortcuts as Blocking or Major findings when their impact matches the target workflow:

- locking a general-purpose main window to a fixed size instead of supporting DPI, font, and workspace changes;
- creating thousands of item-based table/list entries instead of using Model-View;
- using blocking message boxes for routine progress or completion feedback;
- performing I/O or heavy computation in signals, `data()`, or delegate painting;
- restoring docks without stable object names, versioned state, or a usable default layout;
- loading SVG, QSS, or images through development-machine absolute paths;
- declaring a PyInstaller build complete without launching the bundle and checking its resources.

Use `.cursor/rules/qt-ui-engineering/10-hidpi_cross_platform.md` through `14-resource_deploy.md` for the corresponding remediation contracts. These entries apply only to Widget implementations.
