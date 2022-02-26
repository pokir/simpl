setFunctionVar(scope, "print", [&] () {
  if (stack.back().type == 0) std::cout << stack.back().string;
  else if(stack.back().type == 1) std::cout << stack.back().number;
  else if(stack.back().type == 2) std::cout << (stack.back().boolean ? "T" : "F");
});

setFunctionVar(scope, "input", [&] () {
  stack.push_back(Data());
  stack.back().type = 0;
  std::cin >> stack.back().string;
});

setFunctionVar(scope, "system", [&] () {
  stack.push_back((Data) {1, "", (double) std::system(stack.back().string.c_str()), false});
});

setFunctionVar(scope, "stack_size", [&] () {
  stack.push_back((Data){1, "", (double) stack.size(), false});
});

setFunctionVar(scope, "duplicate", [&] () {
  int num = stack.back().number;
  stack.pop_back();
  int size=stack.size();
  for (int i = 0; i < num; ++i) {
    stack.push_back(stack.at(size - num + i));
  }
});

setFunctionVar(scope, "num_to_str", [&] () {
  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {0, std::to_string(temp1.number), 0, false});
});

setFunctionVar(scope, "str_to_num", [&] () {
  temp1 = stack.back();
  stack.pop_back();
  stack.push_back((Data) {1, "", std::stod(temp1.string), false});
});

setFunctionVar(scope, "type_of", [&] () {
  if(stack.back().type == 0) stack.push_back((Data) {0, "str", 0, false});
  else if(stack.back().type == 1) stack.push_back((Data) {0, "num", 0, false});
  else if(stack.back().type == 2) stack.push_back((Data) {0, "bool", 0, false});
  else if(stack.back().type == 3) stack.push_back((Data) {0, "function", 0, false});
});

setFunctionVar(scope, "exit", [&] () {
  std::exit((int) stack.back().number);
});
