SHELL := /bin/bash

.PHONY: default
default: ~/.gitconfig ~/.ondirrc

~/.gitconfig: git/.gitconfig
	rm -f ~/.gitconfig
	ln git/.gitconfig ~/.gitconfig

~/.ondirrc: .ondirrc  # https://makandracards.com/makandra/19549-how-to-set-git-user-and-email-per-directory
	rm -f ~/.ondirrc
	ln .ondirrc ~/.ondirrc
