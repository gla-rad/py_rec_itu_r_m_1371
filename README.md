# The Rec. ITU-R M.1371 Python Package

## Description

The Rec. ITU-R M.1371 Python Package implements elements of Recommendation ITU-R M.1371, 'Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band'.

It has been developed using Python v.3.11.1.

## Installation

1. Ensure [Python](https://www.python.org/downloads/) and the [PDM](https://pdm-project.org/) dependency manager are installed.

1. Clone the GRAD `py_rec_itu_r_m_1371` repository.
    ```
    git clone https://github.com/gla-rad/py_rec_itu_r_m_1371.git
    ```

1. Navigate to the local repository.
    ```
    cd py_rec_itu_r_m_1371
    ```

1. Install the Rec. ITU-R M.1371 package and its dependencies from the `pdm.lock` file.
    ```
    pdm sync --prod
    ```
    Upon successful execution of the above command, `pdm` will generate a virtual Python environment in `./.venv/` and install the package along with its required dependencies into it in *production mode*.

## Code Usage

The main modules of the Rec. ITU-R M.1371 package are located under `./src/rec_itu_r_m_1371/`. The code is structured as outlined below.

For examples of usage, see the source code in this repository and the repositories linked under 'Related Projects'.

### Module: `asm_payloads.py`

This module contains classes for representing the "payload" (the Binary Data portion) of Application Specific Messages (ASM). These payloads can then be embedded either in AIS ASM or VDES-ASM messages.

### Module: `messages.py`

This module includes classes for representing AIS messages and functions for character encoding and decoding, compliant with Rec.
ITU-R M.1371-5, Annex 8.

Currently, support has been implemented for:
* AIS Message 8, 'Binary broadcast message'; and
* AIS Message 21, 'AtoN report'.

## Contributing

We welcome contributions! If you wish to contribute to this project, please follow these steps:

1. Fork the repository and create a new branch.
1. Clone your repository to your local machine.

    ```
    git clone <your_repository_address>
    cd py_rec_itu_r_m_1371
    ```
1. Install the package in *development mode* using PDM.
    ```
    pdm sync --dev
    ```

    Note: The development installation includes dependencies for the [Spyder IDE](https://www.spyder-ide.org/), which may not be necessary if you are using a different IDE.
1. Make your changes and test thoroughly.
1. Submit a pull request with a clear description of your changes.

## Tests

Unit test modules are located under `./tests/`. The chosen testing framework for this project is [pytest](https://pytest.org), included as part of the development installation.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](./LICENSE) file for details.

## Support

Email: Jan.Safar@gla-rad.org

Issue Tracker: [GitHub Issues](https://github.com/gla-rad/py_rec_itu_r_m_1371/issues)

## Related Projects

### Python

* [IEC 61162 package](https://github.com/gla-rad/py_iec_61162.git)
* [IEC 62320 package](https://github.com/gla-rad/py_iec_62320.git)
* [IEC PAS 63343 package](https://github.com/gla-rad/py_iec_pas_63343.git)
* [VDES1000 package](https://github.com/gla-rad/py_vdes1000.git)

### Java

* VDES1000 Library - a Java port of this package, used within the GRAD [e-navigation service framework](https://github.com/orgs/gla-rad/repositories?q=enav) (source code is not yet publicly available).
