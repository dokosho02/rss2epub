class Style():
    def __init__(self):
    
    # defube style
        self.defaultStyle = '''
        BODY { text-align: justify;}
        h1 {
            background-color: lightblue;
            text-align: center;
            text-transform: uppercase;
            font-weight: 200;     
            }
        '''

        self.secondStyle = '''
    @namespace epub "http://www.idpf.org/2007/ops";

    body, p {
        color: blue;
        font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
    }


    h1 {
        text-align: center;
        text-transform: uppercase;
        font-weight: 200;     
    }
    h2 {
        text-align: left;
        text-transform: uppercase;
        font-weight: 200;     
    }

    ol {
            list-style-type: none;
    }

    ol > li:first-child {
            margin-top: 0.3em;
    }


    nav[epub|type~='toc'] > ol > li > ol  {
        list-style-type:square;
    }


    nav[epub|type~='toc'] > ol > li > ol > li {
            margin-top: 0.3em;
    }


    '''
