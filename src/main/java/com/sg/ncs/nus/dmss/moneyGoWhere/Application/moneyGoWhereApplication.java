package com.sg.ncs.nus.dmss.moneyGoWhere.Application;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = {"com.sg.ncs.nus.dmss.moneyGoWhere.*"})
public class moneyGoWhereApplication {
	public static void main(String[] args) {
        SpringApplication.run(moneyGoWhereApplication.class, args);
    }
}
