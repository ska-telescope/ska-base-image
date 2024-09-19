# ska-base-image

This repository contains the definition of the base image that's deprived of application level dependencies for SKAO developers to use as a base image when building their own products or other variant base images.

This will make possible to create and release a security patched Ubuntu 22.04 base image without any application dependencies and to implement a monthly security patch process for all ST services and images.

## Building the image locally

```
make oci-build
```
