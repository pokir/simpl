use std::fs;


#[derive(Debug)]
enum TokenKind {
    Identifier,
    Push,
    Pop,
    Add,
    Subtract,
    Multiply,
    Divide,
    Modulo,
    Equal,
    NotEqual,
    GreaterThan,
    LessThan,
    GreaterThanOrEqualTo,
    LessThanOrEqualTo,
    String,
    Number,
}

#[derive(Debug)]
struct Token {
    kind: TokenKind,
    literal: String,
}

impl Token {
    pub fn new(kind: TokenKind, literal: String) -> Self {
        Self {
            kind,
            literal,
        }
    }
}

#[derive(Debug)]
struct Lexer {
    source: Vec<char>,
    counter: usize,
}

impl Lexer {
    pub fn new(source: String) -> Self {
        Self {
            source: source.chars().collect(),
            counter: 0
        }
    }

    pub fn lex(&mut self) {
        let mut tokens: Vec<Token> = Vec::<Token>::new();

        while self.source.len() > self.counter {
            let c = self.current_char();

            match c {
                '.' => {
                    tokens.push(Token::new(TokenKind::Push, ".".to_owned()));
                    self.counter += 1;
                },
                '@' => {
                    tokens.push(Token::new(TokenKind::Pop, "@".to_owned()));
                    self.counter += 1;
                },
                '+' => {
                    tokens.push(Token::new(TokenKind::Add, "+".to_owned()));
                    self.counter += 1;
                },
                '-' => {
                    tokens.push(Token::new(TokenKind::Subtract, "-".to_owned()));
                    self.counter += 1;
                },
                '*' => {
                    tokens.push(Token::new(TokenKind::Multiply, "*".to_owned()));
                    self.counter += 1;
                },
                '/' => {
                    tokens.push(Token::new(TokenKind::Divide, "/".to_owned()));
                    self.counter += 1;
                },
                '\'' | '"' => {
                    self.counter += 1;
                    
                    let mut buffer: String = String::new();

                    while self.current_char() != c {
                        if self.current_char() == '\\' {
                            self.counter += 1;
                        }

                        buffer.push(self.current_char());

                        self.counter += 1;
                    }

                    println!("{}", buffer);

                    tokens.push(Token::new(TokenKind::String, buffer));
                    self.counter += 1;
                },
                _ if c.is_numeric() => {
                     let mut buffer: String = String::new();

                    buffer.push(c);

                    self.counter += 1;

                    loop {
                        if self.counter > self.source.len() {
                            break;
                        }

                        buffer.push(self.current_char());
                        self.counter += 1;
                    }

                    tokens.push(Token::new(TokenKind::Number, buffer));
                },
                _ if c.is_alphabetic() => {
                    let mut buffer: String = String::new();

                    buffer.push(c);
                    self.counter += 1;

                    while self.current_char().is_alphabetic() {
                        buffer.push(self.current_char());
                        self.counter += 1;
                    }

                    let kind: TokenKind = match buffer.as_str() {
                        // Check for reserved keywords here
                        //"var" => TokenKind::Var,
                        _ => TokenKind::Identifier,
                    };

                    tokens.push(Token::new(kind, buffer));
                },
                _ => {
                    self.counter += 1
                },
            }
        }

        println!("{:?}", tokens);
    }

    fn current_char(&self) -> char {
        *self.source.get(self.counter).unwrap()
    }
}

fn main() {
    let filename = std::env::args().nth(1);
    let filename = if let Some(f) = filename {
        f
    } else {
        panic!("Expected a file.");
    };

    let source = fs::read_to_string(filename);
    let source = if source.is_ok() {
        source.unwrap()
    } else {
        panic!("Could not open file for reading.");
    };

    let mut lexer = Lexer::new(source);
    lexer.lex();
}
