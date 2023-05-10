function getAssertLines(code){
    const lines = code.split(/\r?\n/);
    const assertLineNumbers = [];
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('assert')) {
            assertLineNumbers.push(i);
        }
    }
    return assertLineNumbers;
}


module.exports = {
	getAssertLines
}