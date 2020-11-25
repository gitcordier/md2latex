from constants import *
from utilities import to_string

def copy_all_inputmd(text):
    
    def find_all_inputmd():
        
        def find_closing_after(opening):
            return len(SUBSTRING_OPENING) \
                + text[opening+len(SUBSTRING_OPENING):].find(SUBSTRING_CLOSING) \
                + len(SUBSTRING_CLOSING)
            #
        #
        
        opening = 0
        while True:
            opening = text.find(SUBSTRING_OPENING, opening)
            if opening == -1: 
                return
            #
            else: 
                closing = find_closing_after(opening)
            
                if closing == -1: 
                    return 
                #
                else:
                    closing += opening
                    yield opening, closing 
                
                    opening +=len(SUBSTRING_OPENING)
                #
            #
        #
    # find_all_inputmd: END
    # Nested methods: END ----------------------------------------------------#
    
    blocks = []
    input_ = list(find_all_inputmd())
    #print(L)
    length = len(input_)
    
    if length > 0: 
        opening_last = 0
        closing_last = 0
    
        for i in range(0, length):
            opening_current = input_[i][0]
            closing_current = input_[i][1]
        
            text_before=text[closing_last: opening_current]
            segment   = text[opening_current: closing_current]
            path      = segment[len(SUBSTRING_OPENING):-len(SUBSTRING_CLOSING)]
            #text_after  = text[closing_current:]
            #
            #content_recursive = ''
            with open(path, 'r') as f:
                content_recursive = copy_all_inputmd(f.read())
            #
            blocks.append(text_before)
            blocks.append(content_recursive)
            
            opening_last = opening_current
            closing_last = closing_current
        
        #
        closing_last = input_[-1][1]
        
        text_last  = text[closing_last:]
        blocks.append(text_last)
    
        return to_string(blocks).replace('\\', '√').replace('&', '1729ampersand')
    #
    else:
        return text

# The function clean_up parses a text and return the parsing result.
def clean_up(text: str):
    '''
        input: a text, as a UTF-8 string.
        output: The same text, parsed as follows:
        
        A text , say 
        
        "
            \begin{document}\n
            […]
            Men are born and remain free and equal in rights. 
            <-- Most people forget the second part: --> 
            Social distinctions can be founded only on the common good.
            […]
            √end{document} 
        "
        
        is splitted into text segments, as follows:
            
            ['\begin{document}\n …'],
            …
            ['Men are born and remain free and equal in rights.'], 
            ['% Most people forget the second part:'],
            ['Social distinctions cans be founded only on the common good.']. 
            […]
            [\\end{document}] .
            
        The segments concatenation so provides a LaTeX compliant input:
            
            Men are born and remain free and equal in rights.
            % Most people forget the second part:
            Social distinctions can be founded only on the common good.
    '''
    PLAIN       = 2  # PLAIN = even
    IS_COMMENT  = 3  # COMMENT = odd
    
    #EXPECT_LESS_SIGN = PLAIN
    EXPECT_EXCLAMATION_MARK = 7
    EXPECT_FIRST_DASH = 11
    EXPECT_SECOND_DASH = 13
    EXPECT_GREATER_THAN_SIGN = 17
    
    state = PLAIN
    
    #If a text segment is too long, it is cut into lines.
    MAX_LENGTH_OF_LINE_COMMENT = 80
    MAX_LENGTH_OF_LINE_PLAIN = 72
    
    # RECORD enlists all the segments, as follows:
    #
    #    RECORD = [
    #        #first segment:
    #        [  
    #            [ first line ]
    #                …
    #            [ last line ]
    #        ],
    #        …
    #        #last segment:
    #        [  
    #            [ first line ]
    #                …
    #            [ last line ]
    #        ]
    #   ]
    #
    # A segment is a nonempty list of line(s).
    # A line is a nonempty list of substrings. Most of the time: 'a', …, 'z',….
    #
    RECORD = []
    
    # Getter:
    # last_segment returns the last segment of RECORD. 
    # If RECORD is empty, then an empty list is appended before RECORD[-1] 
    # is called. This way, it is guaranteed that last_segment always returns
    # the last segment RECORD[-1].
    def last_segment():
        if len(RECORD) == 0:
            RECORD.append([])
        else:
            pass
        return RECORD[-1]
    
    # Getter:
    # last_line returns the last line of the last segment of RECORD; see above.
    # If the last segment is empty, then an empty list is appended before
    # last_segment()[-1] is called. This way, it is guaranteed that last_line 
    # always returns the last line RECORD[-1][-1].
    def last_line():
        if len(last_segment()) == 0:
            last_segment().append([])
        else:
            pass
        return last_segment()[-1]
      
    def append(ch):
        # Regular case: Plain text
        if state % 2 == 0:
            if len(last_line()) <= MAX_LENGTH_OF_LINE_PLAIN:
                if ch == '\n':
                    last_segment().append([ch])
                else:
                    last_line().append(ch)
            else:
                if ch == '\n':
                    last_segment().append([ch])
                else:
                    last_line().append(ch)
        # Comment
        elif state %2 !=0:
            # Regular case
            if 0 < len(last_line()) <= MAX_LENGTH_OF_LINE_COMMENT:
                if ch == '\n':
                    last_segment().append(['% '])
                else:
                    last_line().append(ch)  
                #
            #
            elif len(last_line()) > MAX_LENGTH_OF_LINE_COMMENT:
                    last_segment_block().append(['% ' + ch])
                #
            # When the last line is the empty list [], 
            # we fill it with a new content '% […]'.
            # Note that we don't forget to begin the line with '%', the LaTeX 
            # comment mark!
            elif len(last_line()) == 0:
                last_line().append('% ' + e)
            else:
                pass
        else:
            pass
        #
    #
    # Loop: BEGINNING ------------------------------------------------------- #
    for e in text:
        # # # # # # # # # #
        # Plain text case #
        # # # # # # # # # #
        if state is PLAIN:
            if e == '<':
                state = PLAIN * EXPECT_EXCLAMATION_MARK 
            else:
                #state = PLAIN
                append(e)
            #
        elif state is PLAIN * EXPECT_EXCLAMATION_MARK:
            if e == '!':
                state = PLAIN * EXPECT_FIRST_DASH
            else:
                state = PLAIN
                append('<' + e)
            #
        elif state is PLAIN * EXPECT_FIRST_DASH:
            if e == '-':
                state = PLAIN * EXPECT_SECOND_DASH
            else:
                state = PLAIN
                append('<!' + e)
            #
        elif state is PLAIN * EXPECT_SECOND_DASH:
            if e == '-':
                state = IS_COMMENT
                RECORD.append([])
                
            else:
                r
                state = PLAIN
                append('<!-' + e)
        # # # # # # # # # 
        # Inside comment#
        # # # # # # # # # 
        elif state == IS_COMMENT:
            if e == '-':
                state = IS_COMMENT * EXPECT_SECOND_DASH
            else:
                state = IS_COMMENT
                append(e)
            #
        elif state == IS_COMMENT * EXPECT_SECOND_DASH:
            if e == '-':
                state = IS_COMMENT * EXPECT_GREATER_THAN_SIGN
            else:
                state = IS_COMMENT
                append('-' + e)
            #
        elif state == IS_COMMENT*EXPECT_GREATER_THAN_SIGN:
            if e == '>':
                state = PLAIN
                
                # If no content in the last comment line, then we discard it.
                if  last_line() == ['% ']: 
                    last_line().pop()
                else:
                    pass
            else:
                state = IS_COMMENT
                append('--' + e)
        else:
            pass
    # Loop: END --------------------------------------------------------------#
    
    # We return the parsed text
    return to_string(
        
        # to_string(…) concatenates the segments:
        to_string((
        
            # to_string(…) concatenates the line(s) of a segment:
            to_string((
                
                # Turns a line into a \n-terminated string:
                to_string(line), '\n' 
            )) for line in segment
        ))
        for segment in RECORD
    )
#
# END
