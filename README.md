# Lab Data Logger ‒ A (distributed) CLI data logger for the (physics) lab.
[![PyPI](https://img.shields.io/pypi/v/lab_data_recorder?color=blue)](https://pypi.org/project/lab_data_recorder/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A command-line tool that allows logging of data locally or over a network to a InfluxDB. 

## Installation

```
pip install lab_data_recorder
```

## Module diagram
```mermaid
 classDiagram
    class RecorderService{
    queue
    connected_sources
    set_writer()
    connect_source()
    disconnect_source()
    }
    class RandomNumberService{
        <<LabDataService>>
        get_data()
    }
    class ConstNumberService{
        <<LabDataService>>
        get_data()
    }
    class connected_sources{
        Puller
      }
    class Puller1{
        <<Puller>>
        queue
        netloc
        counter
        stop_event
        interval
        measurement
        tags
        requested_fields
        pull_continously()
    }
    class Puller2{
        <<Puller>>
        queue
        netloc
        counter
        stop_event
        interval
        measurement
        tags
        pull_process
        requested_fields
        pull_continously()
    }
      class Writer{
          counter
          write_process
          connect_queue()
          write_continously()
      }
      class Queue{
          Message
          put()
          get()
      }
    RecorderService --* connected_sources
    RecorderService <--> Writer : managing
    Writer <|-- Queue : gets\n Message
    Puller1 --|> Queue : puts \n Message
    Puller2 --|> Queue : puts \n Message
    Puller1 <|-- ConstNumberService : receives \n Message
    Puller1 --> ConstNumberService : queries
    Puller2 <|-- RandomNumberService : receives \n Message
    Puller2 --> RandomNumberService : queries
    connected_sources --* Puller1
    connected_sources --* Puller2

```

## Authors

-   Bastian Leykauf (<https://github.com/bleykauf>)

## License
MIT License

Copyright © 2022 Bastian Leykauf

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
