# rawsync

Cross platform CLI tool for synchronizing raw and jpeg photos between two folders with removing pairless images.

## Usage

### rawsync command

Enter jpeg folder, and execute `rawsync` command. It'll look for a raw folder next to the jpegs, and find
jpeg-raw pairs. After that it'll ask if you want to move pairless jpegs and pairless raws to trash.

### rawpack command

Enter a folder with mixed jpegs and raw files and execute `rawpack`. The tool will try to sort raw files to
a `raw` folder, after asking. 