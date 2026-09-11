const mume = require("@shd101wyy/mume");

async function main() {
    await mume.init();
    const engine = new mume.MarkdownEngine({
        filePath: process.argv[2],
        config: {
            previewTheme: "github-light.css",
            codeBlockTheme: "default.css",
            printBackground: true
        },
    });
    await engine.pandocExport({ runAllCodeChunks: true });
    return process.exit();
}

main().catch(console.error);
