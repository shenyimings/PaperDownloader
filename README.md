# PaperDownloader
A Paper Downloader Powered By Sci-Hub, For Research

> Feature：Input keywords and it'll find Science Papers around the topic sorted by Times Sited, then get them down to your PC via Sci-Hub.

这是申一鸣的高级语言程序设计课设

## Use

Install Requirements:

```bash
pip install -r ./requirements.txt
```

Use

```python
python ./main.py
Please Input Your Keywords >CTF
```

## Develop Log

- Multithreading        Done.
- Modularized           Done.
- Log system            TBD...
- Downloader            Done.
- Paper Finder          Done.

## Some Problems

Sci-Hub deploy DDGuard to Anti DDos attack or high speed spider, this may cause error when downloading.

we use 3 mirror website of Sci-Hub to decrease and distribute the visits, and this may download invalid file, which may differ from mirror to mirror. 

**For Course homework Only.**
