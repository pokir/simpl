/* This file gets included in every simpl program */
/* All comments in this file must be inline */

setFunctionVar(scope, "panic", [&] () {
  if (stack.size() <= 0) {
    std::cout << "Program panicked" << std::endl;
  } else {
    std::cout << "Program panicked: " << stack.back().string << std::endl;
  }

  std::exit(1);
});

setFunctionVar(scope, "print", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "no item on the stack to print";
    getVar(scope, "panic").data.function();
  }

  if (stack.back().type == 0) std::cout << stack.back().string;
  else if(stack.back().type == 1) std::cout << stack.back().number;
  else if(stack.back().type == 2) std::cout << (stack.back().boolean ? "T" : "F");
  else if(stack.back().type == 3) std::cout << "function";
});

setFunctionVar(scope, "input", [&] () {
  stack.push_back(Data());
  stack.back().type = 0;
  std::cin >> stack.back().string;
});

setFunctionVar(scope, "system", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run system because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run system because the argument is not a string";
    getVar(scope, "panic").data.function();
  }

  stack.push_back((Data) {1, "", (double) std::system(stack.back().string.c_str()), false});
});

setFunctionVar(scope, "stack_size", [&] () {
  stack.push_back((Data){1, "", (double) stack.size(), false});
});

setFunctionVar(scope, "duplicate", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run duplicate because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 1) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run duplicate because the argument is not a number";
    getVar(scope, "panic").data.function();
  }

  int num = stack.back().number;
  stack.pop_back();
  int size=stack.size();
  for (int i = 0; i < num; ++i) {
    stack.push_back(stack.at(size - num + i));
  }
});

setFunctionVar(scope, "num_to_str", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run num_to_str because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 1) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run num_to_str because the argument is not a number";
    getVar(scope, "panic").data.function();
  }

  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {0, std::to_string(temp1.number), 0, false});
});

setFunctionVar(scope, "str_to_num", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run str_to_num because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run str_to_num because the argument is not a string";
    getVar(scope, "panic").data.function();
  }

  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {1, "", std::stod(temp1.string), false});
});

setFunctionVar(scope, "bool_to_str", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run bool_to_str because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 2) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run bool_to_str because the argument is not a boolean";
    getVar(scope, "panic").data.function();
  }

  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {0, temp1.boolean ? "T" : "F", 0, false});
});

setFunctionVar(scope, "str_to_bool", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run str_to_bool because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run str_to_bool because the argument is not a string";
    getVar(scope, "panic").data.function();
  }

  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {2, "", 0, temp1.string == "T"});
});

setFunctionVar(scope, "bool_to_num", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run bool_to_num because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 2) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run bool_to_num because the argument is not a boolean";
    getVar(scope, "panic").data.function();
  }

  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {1, "", temp1.boolean ? 1.0 : 0.0, false});
});

setFunctionVar(scope, "num_to_bool", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run num_to_bool because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 1) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run num_to_bool because the argument is not a number";
    getVar(scope, "panic").data.function();
  }

  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {2, "", 0, temp1.number != 0});
});

setFunctionVar(scope, "type_of", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run type_of because the stack is empty";
    getVar(scope, "panic").data.function();
  }

  if(stack.back().type == 0) stack.push_back((Data) {0, "str", 0, false});
  else if(stack.back().type == 1) stack.push_back((Data) {0, "num", 0, false});
  else if(stack.back().type == 2) stack.push_back((Data) {0, "bool", 0, false});
  else if(stack.back().type == 3) stack.push_back((Data) {0, "func", 0, false});
});

setFunctionVar(scope, "exit", [&] () {
  if (stack.size() <= 0) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run exit because the stack is empty";
    getVar(scope, "panic").data.function();
  } else if (stack.back().type != 1) {
    stack.push_back(Data());
    stack.back().type = 0;
    stack.back().string = "can't run exit because the argument is not a number";
    getVar(scope, "panic").data.function();
  }

  std::exit((int) stack.back().number);
});
