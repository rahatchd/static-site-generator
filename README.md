# simple static site generator

write posts in markdown and convert them to a static site

## requirements

- python3.10+

## run

```sh
./main.sh
```

this will change the generated files content, specifically the links to images
and pages will be relative to the github pages url. normally i wouldn't commit
generated files to version control but we need to commit the generated files to
use github pages. i have chosen to live with this for now.

## test

```sh
./test.sh
```

## build

```sh
./build.sh
```

this builds the static site for github pages.

## planned features

- [ ] tokenizer to enable nested inline elements
- [ ] theme support
- [ ] blog generator

## inspiration

[boot.dev](https://www.boot.dev/courses/build-static-site-generator-python)
