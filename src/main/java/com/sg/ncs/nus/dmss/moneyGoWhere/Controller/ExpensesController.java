package com.sg.ncs.nus.dmss.moneyGoWhere.Controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ExpensesController {
	
	@PostMapping("/helloWorld")
	public String helloWorld() {
		return "{\"message\": \"This is a dummy JSON response\"}";
    }
}
