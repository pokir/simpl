#include <cmath>

#include <iostream>

#include <functional>

#include <map>

#include <string>

#include <vector>

struct Data {
  short type;
  std::string string;
  double number;
  bool boolean;
  std:: function < void() > function;
};
struct Variable {
  std::string name;
  Data data;
};
int scope = 0;
std::vector < Data > stack;
std::vector < std::map < std::string, Variable > > variables;
Data temp1;
Data temp2;
bool varExists(int scope, std::string name) {
  for (int i = 0; i <= scope; ++i) {
    if (variables.size() <= i) return false;
    if (variables.at(i).count(name)) return true;
  }
  return false;
}
Variable & getVar(int scope, std::string name) {
  for (int i = 0; i <= scope; ++i) {
    auto found = variables.at(i).find(name);
    if (found != variables.at(i).end()) return found -> second;
  }
}
void setVar(int scope, std::string name, Data data) {
  if (varExists(scope, name)) getVar(scope, name).data = data;
  else {
    while (variables.size() <= scope) variables.push_back(std::map < std::string, Variable > ());
    variables.at(scope).insert_or_assign(name, (Variable) {
      name,
      data
    });
  }
}
void setFunctionVar(int scope, std::string name, std:: function < void() > func) {
  setVar(scope, name, (Data) {
    3,
    "",
    0,
    false,
    func
  });
}
void cleanScopes(int targetScope) {
  while (variables.size() > targetScope + 1) variables.pop_back();
}
int main() {
  setFunctionVar(scope, "print", []() {
    if (stack.back().type == 0) std::cout << stack.back().string;
    else if (stack.back().type == 1) std::cout << stack.back().number;
    else if (stack.back().type == 2) std::cout << (stack.back().boolean ? "T" : "F");
  });
  setFunctionVar(scope, "input", []() {
    stack.push_back(Data());
    stack.back().type = 0;
    std::cin >> stack.back().string;
  });
  setFunctionVar(scope, "system", []() {
    stack.push_back((Data) {
      1,
      "",
      (double) std::system(stack.back().string.c_str()),
      false
    });
  });
  setFunctionVar(scope, "stack_size", []() {
    stack.push_back((Data) {
      1,
      "",
      (double) stack.size(),
      false
    });
  });
  setFunctionVar(scope, "duplicate", []() {
    int num = stack.back().number;
    stack.pop_back();
    int size = stack.size();
    for (int i = 0; i < num; ++i) {
      stack.push_back(stack.at(size - num + i));
    }
  });
  setFunctionVar(scope, "num_to_str", []() {
    temp1 = stack.back();
    stack.pop_back();
    stack.push_back((Data) {
      0,
      std::to_string(temp1.number),
      0,
      false
    });
  });
  setFunctionVar(scope, "str_to_num", []() {
    temp1 = stack.back();
    stack.pop_back();
    stack.push_back((Data) {
      1,
      "",
      std::stod(temp1.string),
      false
    });
  });
  setFunctionVar(scope, "type_of", []() {
    if (stack.back().type == 0) stack.push_back((Data) {
      0,
      "str",
      0,
      false
    });
    else if (stack.back().type == 1) stack.push_back((Data) {
      0,
      "num",
      0,
      false
    });
    else if (stack.back().type == 2) stack.push_back((Data) {
      0,
      "bool",
      0,
      false
    });
  });
  setFunctionVar(scope, "exit", []() {
    std::exit((int) stack.back().number);
  });
  setFunctionVar(scope, "println", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    getVar(scope, "print").data.function();
    cleanScopes(scope);
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "\n";
    getVar(scope, "print").data.function();
    cleanScopes(scope);
    setVar(scope, "_", stack.back());
    stack.pop_back();
  });
  setFunctionVar(scope, "print_stack", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    getVar(scope, "stack_size").data.function();
    cleanScopes(scope);
    setVar(scope, "counter", stack.back());
    stack.pop_back();
    stack.push_back(getVar(scope, "counter").data);
    getVar(scope, "duplicate").data.function();
    cleanScopes(scope);
    while (true) {
      int _scope = scope;
      int scope = _scope + 1;
      stack.push_back(getVar(scope, "counter").data);
      stack.push_back(Data());
      stack.back().type = 1;
      stack.back().number = 0.0;
      temp1 = stack.back();
      stack.pop_back();
      temp2 = stack.back();
      stack.pop_back();
      if (temp1.type != temp2.type || temp1.type != 1) stack.push_back((Data) {
        2,
        "",
        0,
        false
      });
      else if (temp2.number <= temp1.number) stack.push_back((Data) {
        2,
        "",
        0,
        true
      });
      else stack.push_back((Data) {
        2,
        "",
        0,
        false
      });
      if (stack.back().type == 2 && stack.back().boolean) {
        int _scope = scope;
        int scope = _scope + 1;
        setVar(scope, "_", stack.back());
        stack.pop_back();
        break;
      }
      cleanScopes(scope);
      setVar(scope, "_", stack.back());
      stack.pop_back();
      getVar(scope, "println").data.function();
      cleanScopes(scope);
      setVar(scope, "_", stack.back());
      stack.pop_back();
      stack.push_back(getVar(scope, "counter").data);
      stack.push_back(Data());
      stack.back().type = 1;
      stack.back().number = 1.0;
      temp1 = stack.back();
      stack.pop_back();
      temp2 = stack.back();
      stack.back() = (Data) {
        temp1.type, "", temp2.number - temp1.number, false
      };
      setVar(scope, "counter", stack.back());
      stack.pop_back();
    }
    cleanScopes(scope);
  });
  setFunctionVar(scope, "pop", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    setVar(scope, "counter", stack.back());
    stack.pop_back();
    while (true) {
      int _scope = scope;
      int scope = _scope + 1;
      stack.push_back(getVar(scope, "counter").data);
      stack.push_back(Data());
      stack.back().type = 1;
      stack.back().number = 0.0;
      temp1 = stack.back();
      stack.pop_back();
      temp2 = stack.back();
      stack.pop_back();
      if (temp1.type != temp2.type || temp1.type != 1) stack.push_back((Data) {
        2,
        "",
        0,
        false
      });
      else if (temp2.number <= temp1.number) stack.push_back((Data) {
        2,
        "",
        0,
        true
      });
      else stack.push_back((Data) {
        2,
        "",
        0,
        false
      });
      if (stack.back().type == 2 && stack.back().boolean) {
        int _scope = scope;
        int scope = _scope + 1;
        setVar(scope, "_", stack.back());
        stack.pop_back();
        break;
      }
      cleanScopes(scope);
      setVar(scope, "_", stack.back());
      stack.pop_back();
      stack.push_back(getVar(scope, "counter").data);
      stack.push_back(Data());
      stack.back().type = 1;
      stack.back().number = 1.0;
      temp1 = stack.back();
      stack.pop_back();
      temp2 = stack.back();
      stack.back() = (Data) {
        temp1.type, "", temp2.number - temp1.number, false
      };
      setVar(scope, "counter", stack.back());
      stack.pop_back();
    }
    cleanScopes(scope);
  });
  setFunctionVar(scope, "flip", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
  });
  setFunctionVar(scope, "is_str", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    getVar(scope, "type_of").data.function();
    cleanScopes(scope);
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "str";
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.pop_back();
    if (temp1.type != temp2.type) stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
    else if ((temp1.type == 0 && temp1.string == temp2.string) || (temp1.type == 1 && temp1.number == temp2.number) || (temp1.type == 2 && temp1.boolean == temp2.boolean)) stack.push_back((Data) {
      2,
      "",
      0,
      true
    });
    else stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
  });
  setFunctionVar(scope, "is_num", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    getVar(scope, "type_of").data.function();
    cleanScopes(scope);
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "num";
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.pop_back();
    if (temp1.type != temp2.type) stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
    else if ((temp1.type == 0 && temp1.string == temp2.string) || (temp1.type == 1 && temp1.number == temp2.number) || (temp1.type == 2 && temp1.boolean == temp2.boolean)) stack.push_back((Data) {
      2,
      "",
      0,
      true
    });
    else stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
  });
  setFunctionVar(scope, "is_bool", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    getVar(scope, "type_of").data.function();
    cleanScopes(scope);
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "bool";
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.pop_back();
    if (temp1.type != temp2.type) stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
    else if ((temp1.type == 0 && temp1.string == temp2.string) || (temp1.type == 1 && temp1.number == temp2.number) || (temp1.type == 2 && temp1.boolean == temp2.boolean)) stack.push_back((Data) {
      2,
      "",
      0,
      true
    });
    else stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
  });
  setFunctionVar(scope, "floor", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    stack.push_back(Data());
    stack.back().type = 1;
    stack.back().number = 1.0;
    getVar(scope, "duplicate").data.function();
    cleanScopes(scope);
    stack.push_back(Data());
    stack.back().type = 1;
    stack.back().number = 1.0;
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.back() = (Data) {
      temp1.type, "", std::fmod(temp2.number, temp1.number), false
    };
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.back() = (Data) {
      temp1.type, "", temp2.number - temp1.number, false
    };
  });
  setFunctionVar(scope, "ceil", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    getVar(scope, "floor").data.function();
    cleanScopes(scope);
    stack.push_back(Data());
    stack.back().type = 1;
    stack.back().number = 1.0;
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.back() = (Data) {
      temp1.type, temp2.string + temp1.string, temp2.number + temp1.number, false
    };
  });
  setFunctionVar(scope, "round", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    stack.push_back(Data());
    stack.back().type = 1;
    stack.back().number = 0.5;
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.back() = (Data) {
      temp1.type, temp2.string + temp1.string, temp2.number + temp1.number, false
    };
    getVar(scope, "floor").data.function();
    cleanScopes(scope);
  });
  setFunctionVar(scope, "pow", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    setVar(scope, "exponent", stack.back());
    stack.pop_back();
    setVar(scope, "base", stack.back());
    stack.pop_back();
    stack.push_back(getVar(scope, "exponent").data);
    setVar(scope, "counter", stack.back());
    stack.pop_back();
    stack.push_back(Data());
    stack.back().type = 1;
    stack.back().number = 1.0;
    stack.push_back(getVar(scope, "exponent").data);
    stack.push_back(Data());
    stack.back().type = 1;
    stack.back().number = 0.0;
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.pop_back();
    if (temp1.type != temp2.type || temp1.type != 1) stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
    else if (temp2.number >= temp1.number) stack.push_back((Data) {
      2,
      "",
      0,
      true
    });
    else stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
    if (stack.back().type == 2 && stack.back().boolean) {
      int _scope = scope;
      int scope = _scope + 1;
      setVar(scope, "_", stack.back());
      stack.pop_back();
      while (true) {
        int _scope = scope;
        int scope = _scope + 1;
        stack.push_back(getVar(scope, "counter").data);
        stack.push_back(Data());
        stack.back().type = 1;
        stack.back().number = 0.0;
        temp1 = stack.back();
        stack.pop_back();
        temp2 = stack.back();
        stack.pop_back();
        if (temp1.type != temp2.type || temp1.type != 1) stack.push_back((Data) {
          2,
          "",
          0,
          false
        });
        else if (temp2.number <= temp1.number) stack.push_back((Data) {
          2,
          "",
          0,
          true
        });
        else stack.push_back((Data) {
          2,
          "",
          0,
          false
        });
        if (stack.back().type == 2 && stack.back().boolean) {
          int _scope = scope;
          int scope = _scope + 1;
          setVar(scope, "_", stack.back());
          stack.pop_back();
          break;
        }
        cleanScopes(scope);
        setVar(scope, "_", stack.back());
        stack.pop_back();
        stack.push_back(getVar(scope, "counter").data);
        stack.push_back(Data());
        stack.back().type = 1;
        stack.back().number = 1.0;
        temp1 = stack.back();
        stack.pop_back();
        temp2 = stack.back();
        stack.back() = (Data) {
          temp1.type, "", temp2.number - temp1.number, false
        };
        setVar(scope, "counter", stack.back());
        stack.pop_back();
        stack.push_back(getVar(scope, "base").data);
        temp1 = stack.back();
        stack.pop_back();
        temp2 = stack.back();
        stack.back() = (Data) {
          temp1.type, "", temp2.number * temp1.number, false
        };
      }
      cleanScopes(scope);
      return;
    }
    cleanScopes(scope);
    setVar(scope, "_", stack.back());
    stack.pop_back();
    stack.push_back(getVar(scope, "exponent").data);
    stack.push_back(Data());
    stack.back().type = 1;
    stack.back().number = 0.0;
    temp1 = stack.back();
    stack.pop_back();
    temp2 = stack.back();
    stack.pop_back();
    if (temp1.type != temp2.type || temp1.type != 1) stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
    else if (temp2.number < temp1.number) stack.push_back((Data) {
      2,
      "",
      0,
      true
    });
    else stack.push_back((Data) {
      2,
      "",
      0,
      false
    });
    if (stack.back().type == 2 && stack.back().boolean) {
      int _scope = scope;
      int scope = _scope + 1;
      setVar(scope, "_", stack.back());
      stack.pop_back();
      stack.push_back(getVar(scope, "counter").data);
      stack.push_back(Data());
      stack.back().type = 1;
      stack.back().number = -1.0;
      temp1 = stack.back();
      stack.pop_back();
      temp2 = stack.back();
      stack.back() = (Data) {
        temp1.type, "", temp2.number * temp1.number, false
      };
      setVar(scope, "counter", stack.back());
      stack.pop_back();
      while (true) {
        int _scope = scope;
        int scope = _scope + 1;
        stack.push_back(getVar(scope, "counter").data);
        stack.push_back(Data());
        stack.back().type = 1;
        stack.back().number = 0.0;
        temp1 = stack.back();
        stack.pop_back();
        temp2 = stack.back();
        stack.pop_back();
        if (temp1.type != temp2.type || temp1.type != 1) stack.push_back((Data) {
          2,
          "",
          0,
          false
        });
        else if (temp2.number <= temp1.number) stack.push_back((Data) {
          2,
          "",
          0,
          true
        });
        else stack.push_back((Data) {
          2,
          "",
          0,
          false
        });
        if (stack.back().type == 2 && stack.back().boolean) {
          int _scope = scope;
          int scope = _scope + 1;
          setVar(scope, "_", stack.back());
          stack.pop_back();
          break;
        }
        cleanScopes(scope);
        setVar(scope, "_", stack.back());
        stack.pop_back();
        stack.push_back(getVar(scope, "counter").data);
        stack.push_back(Data());
        stack.back().type = 1;
        stack.back().number = 1.0;
        temp1 = stack.back();
        stack.pop_back();
        temp2 = stack.back();
        stack.back() = (Data) {
          temp1.type, "", temp2.number - temp1.number, false
        };
        setVar(scope, "counter", stack.back());
        stack.pop_back();
        stack.push_back(getVar(scope, "base").data);
        temp1 = stack.back();
        stack.pop_back();
        temp2 = stack.back();
        stack.back() = (Data) {
          temp1.type, "", temp2.number / temp1.number, false
        };
      }
      cleanScopes(scope);
      return;
    }
    cleanScopes(scope);
    setVar(scope, "_", stack.back());
    stack.pop_back();
  });
  setFunctionVar(scope, "func", [ & scope]() {
    int _scope = scope;
    int scope = _scope + 1;
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "hi!";
    getVar(scope, "println").data.function();
    cleanScopes(scope);
    setFunctionVar(scope, "other", [ & scope]() {
      int _scope = scope;
      int scope = _scope + 1;
      stack.push_back(Data());
      stack.back().type = 0;
      stack.back().string = "wow!";
      getVar(scope, "println").data.function();
      cleanScopes(scope);
    });
    getVar(scope, "other").data.function();
    cleanScopes(scope);
  });
  getVar(scope, "func").data.function();
  cleanScopes(scope);
  return 0;
}
